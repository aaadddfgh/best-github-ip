import tempfile
import os

from utils.HostsManage import HostsManager




def test_hosts_manager():
    # 创建临时文件
    # with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
    #     tmp.write("# Original content\n")
    #     tmp_path = tmp.name
    tmp_path="hosts.txt"
    try:
        # 使用临时文件初始化
        manager = HostsManager()

        # 测试添加映射
        manager.add_mapping("127.0.0.1", ["test.host"])
        assert "test.host" in manager.get_program_controlled_mappings().get("127.0.0.1", [])


        # 测试删除映射
        # manager.remove_mapping("127.0.0.1", ["test.host"])
        # assert "127.0.0.1" not in manager.get_program_controlled_mappings()

    finally:
        pass
        #os.remove(tmp_path)

if __name__ == "__main__":
    test_hosts_manager()
    print("所有测试通过！")