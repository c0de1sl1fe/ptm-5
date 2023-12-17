import pytest
import os
import shutil
import zipfile


from utils import InterfaceFileOperation


path_dict = {
    "root": "test_folder",
    "src": os.path.join("test_folder", "src"),
    "dst": os.path.join("test_folder", "dst"),
    "non_exist_src": os.path.join("test_folder", "non_exist_src"),
    "non_exist_dst": os.path.join("test_folder", "non_exist_dst"),
    "src_1": os.path.join("test_folder", "src_1"),
    "file": os.path.join(os.path.join("test_folder", "src"), "file.txt"),
    "file_copy": os.path.join(os.path.join("test_folder", "dst"), "file.txt"),
    "file_rec": os.path.join(os.path.join("test_folder", "src_1"), "file.txt"),
}


@pytest.fixture
def intervace() -> InterfaceFileOperation:
    """
    The function for creating an instance InterfaceFileOperation for testing
    Returns InterfaceFileOperation
    """
    return InterfaceFileOperation()


@pytest.fixture()
def create_tmp_dir():
    """ fixture for craete test folder and then remove it"""

    if os.path.exists(path_dict["root"]):
        shutil.rmtree(path_dict["root"])

    os.mkdir(path_dict["root"])
    os.mkdir(path_dict["src_1"])
    os.mkdir(path_dict["src"])
    os.mkdir(path_dict["dst"])
    with open(path_dict["file"], "w") as file:
        file.write("test")
    yield path_dict

    shutil.rmtree(path_dict["root"])


@pytest.mark.parametrize("src, dst, expected", [(path_dict["src_1"], path_dict["dst"], True), (path_dict["non_exist_src"], path_dict["non_exist_dst"], False), (path_dict["src"], path_dict["dst"], False)])
def test_cmp_folder(intervace: InterfaceFileOperation, create_tmp_dir, src: str, dst: str, expected: bool):
    """test copy folder function"""

    assert intervace.cmp_folder(src, dst) == expected


def test_full_backup(intervace: InterfaceFileOperation, create_tmp_dir):
    """test copy function"""

    # copy exists
    intervace.full_backup(create_tmp_dir["src"], create_tmp_dir["dst"])
    assert os.path.isfile(create_tmp_dir["file_copy"]) == True

    # copy from non exists
    assert intervace.full_backup(
        create_tmp_dir["non_exist_src"], create_tmp_dir["dst"]) == False


@pytest.mark.parametrize("name , expected", [(path_dict["src"], True), (path_dict["non_exist_dst"], False)])
def test_is_dir(intervace: InterfaceFileOperation, create_tmp_dir, name: str, expected: bool):
    """test is dir function"""
    assert intervace.is_dir(name) == expected


def test_rename_folder(intervace: InterfaceFileOperation, create_tmp_dir):
    """test rename function folder"""
    #
    new_name = create_tmp_dir["src_1"][:-1] + "2"
    new_name_2 = create_tmp_dir["non_exist_src"] + "_2"
    assert intervace.rename_folder(new_name, create_tmp_dir["src_1"]) == True
    assert os.path.exists(new_name) == True

    # non exists folders rename
    assert intervace.rename_folder(
        new_name_2, create_tmp_dir["non_exist_src"]) == False
    assert os.path.exists(new_name_2) == False


def test_recover(intervace: InterfaceFileOperation, create_tmp_dir):
    intervace.recover(create_tmp_dir["src"], create_tmp_dir["src_1"])
    assert os.path.exists(create_tmp_dir["file_rec"])


def test_create_name(intervace: InterfaceFileOperation, create_tmp_dir):
    """test create name function"""
    assert intervace.create_name(create_tmp_dir["src"], create_tmp_dir["dst"])


def test_zipping(intervace: InterfaceFileOperation, create_tmp_dir):
    """test zipping function, 
    if input path ith file return path to zip in that folder
    if input zip return itself
    """
    path = intervace.ziping(create_tmp_dir["src"])
    assert zipfile.is_zipfile(path) == True
    assert intervace.ziping(path) == path


if __name__ == '__main__':
    pytest.main(["-v", "-color=yes"])
