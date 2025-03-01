from kgr.project import KangarooProject


def test_init_kgr_project(tmp_path):
    project = KangarooProject(tmp_path)
    assert project.name == tmp_path.name
    assert project.kgr_folder_path() == tmp_path / '.kgr'
    assert project.kgr_folder_path().exists() is False
    assert project.initialize() is True
    assert project.kgr_folder_path().exists() is True
    # finally, test that we cannot initialize the project again
    assert project.initialize() is False
