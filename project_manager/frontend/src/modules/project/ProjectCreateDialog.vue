<template lang="">
  <v-dialog v-model="dialog" persistent max-width="1100px" scrollable>
    <template v-slot:activator="{ on, attrs }">
      <div v-bind="attrs" v-on="on">
        <slot name="btn"></slot>
      </div>
    </template>
    <v-card>
      <v-card-title>
        <span v-if="project?.id" class="text-h5 font-weight-bold">Edit Project</span>
        <span v-else class="text-h5 font-weight-bold">Create Project</span>
        <v-card-actions>
          <v-btn color="blue darken-1" icon @click="close" absolute right>
            <v-icon color="#ccc" size="34">mdi-close-circle</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card-title>
      <div class="d-flex align-center" style="height: 500px">
        <v-stepper :value="step" vertical class="elevation-0" style="width: 250px; letter-spacing: 1px" non-linear>
          <v-stepper-step :complete="step > 1" step="1">
            Project Info <small>Enter Project Info</small>
          </v-stepper-step>
          <v-stepper-content step="1" class="my-3"> </v-stepper-content>
          <v-stepper-step :complete="step > 2" step="2"> Dataset <small>Select Dataset</small> </v-stepper-step>
          <v-stepper-content step="2" class="my-3"></v-stepper-content>
          <v-stepper-step :complete="step > 3" step="3"> Target <small>Select Target</small> </v-stepper-step>
          <v-stepper-content step="3" class="my-3"></v-stepper-content>
          <v-stepper-step step="4"> Configuration <small>Select Configuration</small> </v-stepper-step>
          <v-stepper-content step="4" class="mt-2"></v-stepper-content>
        </v-stepper>
        <div style="width: 75%; height: 500px" class="px-10">
          <FirstStepper v-if="step === 1" @next="next" />
          <SecondStepper v-else-if="step === 2" @next="next" @prev="prev" />
          <ThirdStepper v-else-if="step === 3" @next="next" @prev="prev" />
          <FourthStepper v-else @prev="prev" @create="create" />
        </div>
      </div>
    </v-card>
  </v-dialog>
</template>
<script>
import { mapMutations, mapState } from "vuex";
import { ProjectNamespace, ProjectMutations } from "@/store/modules/project";

import FirstStepper from "./stepper/FirstStepper.vue";
import SecondStepper from "./stepper/SecondStepper.vue";
import ThirdStepper from "./stepper/ThirdStepper.vue";
import FourthStepper from "./stepper/FourthStepper.vue";

import { /*TaskType,*/ ContainerName } from "@/shared/enums";

import { updateProjectInfo, setWorkflow } from "@/api";

export default {
  components: { FirstStepper, SecondStepper, ThirdStepper, FourthStepper },

  props: {
    step: {
      default: 1
    }
  },

  data() {
    return {
      dialog: false
    };
  },

  computed: {
    ...mapState(ProjectNamespace, ["project"])
  },

  mounted() {
    this.$EventBus.$on("forcedTermination", () => {
      this.dialog = false;
      this.$emit("stepChange", 1);
      this.$emit("close");
    });
  },

  beforeDestroy() {
    this.INIT_PROJECT();
  },

  methods: {
    ...mapMutations(ProjectNamespace, {
      SET_PROJECT: ProjectMutations.SET_PROJECT,
      INIT_PROJECT: ProjectMutations.INIT_PROJECT
    }),

    async next(data) {
      if (this.step !== 4) {
        this.$emit("stepChange", this.step + 1);
      }
      this.SET_PROJECT(data);

      if (this.project.id) {
        const param = {
          project_id: this.project.id,
          project_target: this.project.target_id || "",
          project_dataset: this.project.dataset || "",
          task_type: this.project.task_type || "",
          autonn_dataset_file: this.project.autonn_dataset_file || "",
          autonn_base_model: this.project.autonn_basemodel || "",
          nas_type: this.project.nas_type || "",
          deploy_weight_level: this.project.deploy_weight_level || "",
          deploy_precision_level: this.project.deploy_precision_level || "",
          deploy_processing_lib: this.project.deploy_processing_lib || "",
          deploy_user_edit: this.project.deploy_user_edit || "no",
          deploy_input_method: this.project.deploy_input_method || "",
          deploy_input_data_path: this.project.deploy_input_data_path || "",
          deploy_output_method: this.project.deploy_output_method || "0",

          deploy_input_source: this.project.deploy_input_source || "0"
        };

        await updateProjectInfo(param);
      }
    },

    prev() {
      if (this.step !== 1) {
        this.$emit("stepChange", this.step - 1);
      }
    },

    async create(data) {
      this.SET_PROJECT(data);

      const param = {
        project_id: this.project.id,
        project_target: this.project.target_id,
        project_dataset: this.project.dataset,
        task_type: this.project.task_type,
        autonn_dataset_file: this.project.autonn_dataset_file,
        autonn_base_model: this.project.autonn_basemodel,
        nas_type: this.project.nas_type,
        deploy_weight_level: this.project.deploy_weight_level,
        deploy_precision_level: this.project.deploy_precision_level,
        deploy_processing_lib: this.project.deploy_processing_lib,
        deploy_user_edit: this.project.deploy_user_edit || "no",
        deploy_input_method: this.project.deploy_input_method,
        deploy_input_data_path: this.project.deploy_input_data_path,
        deploy_output_method: this.project.deploy_output_method || "0",

        deploy_input_source: this.project.deploy_input_source || "0"
      };

      await updateProjectInfo(param);

      // 20240610........ 이전 버전...................
      // const workflow =
      //   this.project.task_type === TaskType.DETECTION
      //     ? [ContainerName.BMS, ContainerName.AUTO_NN, ContainerName.CODE_GEN, ContainerName.IMAGE_DEPLOY]
      //     : [
      //         ContainerName.BMS,
      //         ContainerName.VISUALIZATION,
      //         ContainerName.AUTO_NN_RESNET,
      //         ContainerName.CODE_GEN,
      //         ContainerName.IMAGE_DEPLOY
      //       ];

      // const workflow =
      //   this.project.task_type === TaskType.DETECTION
      //     ? [ContainerName.AUTO_NN, ContainerName.CODE_GEN, ContainerName.IMAGE_DEPLOY]
      //     : [
      //         // ContainerName.VISUALIZATION,
      //         ContainerName.AUTO_NN_RESNET,
      //         ContainerName.CODE_GEN,
      //         ContainerName.IMAGE_DEPLOY
      //       ];

      const workflow = [ContainerName.AUTO_NN, ContainerName.CODE_GEN, ContainerName.IMAGE_DEPLOY];

      if (this.project.deploy_user_edit === "yes") {
        workflow.splice(workflow.length - 1, 0, ContainerName.USER_EDITING);
      }

      await setWorkflow(this.project.id, workflow);
      if (this.$route.params?.id) {
        this.$router.go();
      } else {
        this.$router.push(`project/${this.project.id}`);
      }
      this.close();
    },

    close() {
      this.dialog = false;
      this.$emit("stepChange", 1);
      this.$emit("close");
      this.INIT_PROJECT();
    }
  }
};
</script>
<style lang="scss" scoped></style>
