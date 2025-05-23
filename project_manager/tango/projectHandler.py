import os
import requests
import asyncio
import docker
# import zipfile
import shutil
import json
import textwrap

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(os.path.dirname(BASE_DIR))

#region API REQUEST ...................................................................................................

async def start_handler(continer, user_id, project_id, target_info):
    """
    Container Start Request Handler

    Args:
        continer : continer
        user_id : user_id
        project_id : project_id
        target_info : If the container is imagedenploy, receive hostname and port as targetinfo

    Returns:
        request info
    """

    if continer != 'imagedeploy':
        host, port = get_container_info(continer)
    else :
        host, port = get_deploy_host_port(target_info)

    print("continer_start_api : " + host + ':' + port)

    start_task = asyncio.create_task(continer_start_api(host + ':' + port, user_id, project_id))
    result = await start_task
    # host, port = get_container_info(continer)
    # result = continer_start_api(host + ':' + port, user_id, project_id)
    return result

async def continer_start_api(host, user_id, project_id):
    """
    Request start API

    Args:
        host : hostname (Defined in docker-compose.yml) 
        user_id : user_id
        project_id : project_id

    Returns:
        request info
    """

    url = 'http://' + host + '/start'
    headers = {
        'Content-Type' : 'text/plain'
    }
    payload = {
        'user_id' : user_id,
        'project_id' : project_id,
    }
    response = requests.get(url, headers=headers, params=payload)
    print_roundtrip_text = print_roundtrip(response, "Start", host)

    # return response.json()
    # return str(response.content.decode('utf-8'))
    return json.dumps({'response': str(response.content, 'utf-8').replace('"',''), 'request_info': str(print_roundtrip_text)})



#################################################################################################################

async def request_handler(continer, user_id, project_id, target_info):
    """
    Container task Status Request Handler

    Args:
        continer : continer
        user_id : user_id
        project_id : project_id
        target_info : If the container is imagedenploy, receive hostname and port as targetinfo

    Returns:
        request info
    """

    # host, port = get_container_info(continer)
    # start_task = asyncio.create_task(continer_request_api(host + ':' + port, user_id, project_id))
    # result = await start_task
    try:
        # host, port = get_container_info(continer)
        # result = continer_request_api(host + ':' + port, user_id, project_id)
        # return result


        # host, port = get_container_info(continer)
        if continer != 'imagedeploy':
            host, port = get_container_info(continer)
        else :
            host, port = get_deploy_host_port(target_info)

        print("continer_start_api : " + host + ':' + port)

        start_task = asyncio.create_task(continer_request_api(host + ':' + port, user_id, project_id))
        result = await start_task
        return result
    
    except Exception as error:
        print('request_handler - error : ' + str(error))
        return None

async def continer_request_api(host, user_id, project_id):
    """
    Request container status API

    Args:
        host : hostname (Defined in docker-compose.yml) 
        user_id : user_id
        project_id : project_id

    Returns:
        request info
    """
        
    url = 'http://' + host + '/status_request'
    headers = {
        'Content-Type' : 'text/plain'
    }
    payload = {
        'user_id' : user_id,
        'project_id' : project_id,
    }
    response = requests.get(url, headers=headers, params=payload, timeout = 5)
    print_roundtrip_text = print_roundtrip(response, "Status Request", host)

    # return response.json()
    # return str(response.content.decode('utf-8'))
    # return str(response.content, 'utf-8').replace('"','')
    return json.dumps({'response': str(response.content, 'utf-8').replace('"',''), 'request_info': str(print_roundtrip_text)})


#endregion

#region Get Docker Logs ...............................................................................................

def get_docker_log_handler(container, last_logs_timestamp):
    """
    Docker-compose log Get function

    Args:
        container : container
        last_logs_timestamp(int) : Finally, the time stamp that received the docker log

    Returns:
        docker log
    """

    client = docker.from_env()
    dockerContainerName = get_docker_container_name(container)
    containerList = client.containers.list()
    container = next(item for item in containerList if dockerContainerName in str(item.name))
    logs = ''
    if int(last_logs_timestamp) == 0:
        logs = container.logs(timestamps = True)
    else:
        logs = container.logs(timestamps = True, since = int(last_logs_timestamp))
    if logs == None:
        return ''
    return logs.decode('utf-8')
#endregion

#region Get Container Info ............................................................................................
def get_container_info(host_name):
    """
    Get ports into hostname

    Args:
        host : hostname (Defined in docker-compose.yml) 

    Returns:
        hostname, port
    """

    ports_by_container = {
        'bms' : "8081",
        'autonn' : "8100",
        'yoloe' : "8090",
        'codeGen' : "8888",
        'autonn-resnet': "8092",
        'viz2code': "8091"
    }
    return host_name, ports_by_container[host_name]

def get_docker_container_name(container):
    """
    Get docker container name

    Args:
        container : container ID

    Returns:
        container name
    """

    containerName = ''
    if container == 'init' :
        containerName = ''
    elif container == 'bms' :
        containerName = 'bms'
    elif container == 'autonn' :
        containerName = 'autonn'
    elif container == 'yoloe' :
        containerName = 'autonn_yoloe'
    elif container == 'labelling' :
        containerName = 'labelling'
    elif container == 'autonn-resnet' :
        containerName = 'autonn_resnet'
    elif container == 'autonn_bb' :
        containerName = 'autonn_bb'
    elif container == 'autonn_nk' :
        containerName = 'autonn_nk'
    elif container == 'codeGen' :
        containerName = 'code_gen'
    elif container == 'k8s' :
        containerName = 'tango_k8s'
    elif container == 'ondevice' or container == 'ondevice_deploy':
        containerName = 'ondevice_deploy'
    elif container == 'viz2code':
        containerName = 'viz2code'
    else :
        containerName = 'bms'

    return str(containerName)

def get_deploy_host_port(deploy_type):
    """
    Get host name and port with target info for image deployment

    Args:
        deploy_type : deploy_type (Defined in shared/common/user_id/project_id/projct_info.yaml)

    Returns:
        host name, port
    """

    port = ''
    if deploy_type == 'Cloud' :
        return "cloud-deploy", "8890"
    elif deploy_type == 'K8S' or deploy_type == 'K8S_Jetson_Nano':
        return "kube-deploy", "8901"
    else:
        # ondevice 등등.... 
        return "ondevice", "8891"
#endregion


def print_roundtrip(response, path, container):
    """
    Transform function to display API call result as log

    Args:
        response : response
        path : response
        container : response

    Returns:
        display log
    """

    format_headers = lambda d: '\n'.join(f'{k}: {v}' for k, v in d.items())

    return str(textwrap.dedent('''
        ---------------- {path} ----------------
        Project Manager --> {container}
        {req.method} {req.url}
        {reqhdrs}
        ---------------- response ----------------
        {res.status_code} {res.reason} {res.url}
        {reshdrs}

        response : {res.text}
        ------------------------------------------
    ''').format(
        req=response.request, 
        res=response, 
        reqhdrs=format_headers(response.request.headers), 
        reshdrs=format_headers(response.headers), 
        path=path,
        container=container
    ))

# 로그에 보여질 Container 명으로 변경
def get_log_container_name(container):
    """
    Name of the container to be displayed in the log
    (Actions to unify as one when displayed in the log)

    Args:
        container : container

    Returns:
        string
    """

    if container == 'bms':
        return 'BMS'
    elif container == 'yoloe' or container == 'autonn-resnet' or container == 'autonn':
        return 'Auto NN'
    elif container == 'codeGen' or container == 'code_gen' or container == 'codegen':
        return 'Code Gen'
    elif container == 'imagedeploy':
        return 'Image Deploy'
    elif container == 'viz2code':
        return 'viz2code'
    

def db_container_name(container):
    """
    Get the name of the container to store in the database

    Args:
        container : container

    Returns:
        string
    """

    if container == 'bms':
        return 'bms'
    elif container == 'autonn':
        return 'autonn'
    elif container == 'yoloe':
        return 'yoloe'
    elif container == 'viz2code' or container == 'visualization':
        return 'viz2code'
    elif container == 'autonn-resnet':
        return 'autonn-resnet'
    elif container == 'codeGen' or container == 'code_gen' or container == 'codegen':
        return 'codeGen'
    elif container == 'ondevice_deploy' or container == 'kube_deploy' or container == 'cloud_deploy':
        return 'imagedeploy'

def nn_model_zip(user_id, project_id):
    """
    Convert path to zip file to shared/common/user_id/project_id/nn_model

    Args:
        user_id : user_id
        project_id : project_id

    Returns:
        zip file
    """

    file_path = os.path.join(root_path, "shared/common/{0}/{1}".format(str(user_id), str(project_id)))
    os.chdir(file_path)

    print("start folder_zip shutil")
    print("file_path  : " + str(file_path))
    print(os.walk(os.path.join(file_path, 'nn_model')))

    a = shutil.make_archive("nn_model", 'zip', os.path.join(file_path, "nn_model"))
    print(a)

    print("end folder_zip")


    return os.path.join(file_path, "nn_model.zip")

def nn_model_unzip(user_id, project_id, file):
    """
    unzip file

    Args:
        user_id : user_id
        project_id : project_id
        file : zip file

    Returns:
        zip file
    """
    file_path = os.path.join(root_path, "shared/common/{0}/{1}".format(str(user_id), str(project_id)))
    save_path = os.path.join(file_path, 'nn_model.zip')

    with open(save_path, 'wb') as destination_file:
        for chunk in file.chunks():
            destination_file.write(chunk)

    filename = save_path
    extrack_dir = os.path.join(file_path, 'nn_model')
    archive_format = "zip"

    shutil.unpack_archive(filename, extrack_dir, archive_format)

    return os.path.join(file_path, "nn_model.zip")

def create_text_file_if_not_exists(file_path):
    """
    create text file if not exists

    Args:
        file_path : file_path        
    """
    try:
        # Try to open the file in read mode to check if it exists
        with open(file_path, 'r'):
            pass
    except FileNotFoundError:
        # If the file doesn't exist, create it
        with open(file_path, 'w') as f:
            f.write("This is a new text file.")
        print(f"File '{file_path}' created.")

def update_project_log_file(user_id, project_id, log):
    """
    Add/save log to shared/common/user_id/project_id/log.txt file

    Args:
        user_id : user_id        
        project_id : project_id        
        log : Log to update
    """
        
    log_file_path = os.path.join(root_path, "shared/common/{0}/{1}".format(str(user_id), str(project_id)), 'log.txt')
    # create_text_file_if_not_exists(log_file_path)

    with open(log_file_path, 'a+') as f:
        f.write(log)


def findIndexByDicList(list, find_column, find_value):
    """
    Finds the index of a dictionary in a list of dictionaries, where the value of the specified column matches the specified value.

    Args:
        list: A list of dictionaries.
        find_column: The column name to search for the match.
        find_value: The value to match against.

    Returns:
        The index of the matching dictionary, or `None` if no match is found.
    """

    index = None
    for i, person in enumerate(list):
        print(person[find_column])
        print(find_value)
        if person[find_column] == find_value:
            index = i
            break
    
    return index
# def db_container_name(container):
#     if container == 'bms' or container == 'BMS':
#         return 'bms'
#     elif container == 'yoloe':
#         return 'yoloe'
#     elif container == 'codeGen' or container == 'code_gen' or container == 'codegen':
#         return 'codeGen'