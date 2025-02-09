import re
import platform

def get_default_hosts_path():
    """获取系统默认的 hosts 文件路径"""
    system = platform.system()
    if system == "Windows":
        return "C:\\Windows\\System32\\drivers\\etc\\hosts"
    else:
        return "/etc/hosts"

class HostsManager:
    def __init__(self, hosts_file=None):
        """
        初始化 HostsManager
        :param hosts_file: hosts 文件路径，默认为系统默认路径
        """
        self.hosts_file = hosts_file or get_default_hosts_path()
        self.BEGIN_MARKER = "# BEGIN PROGRAM CONTROL"
        self.END_MARKER = "# END PROGRAM CONTROL"

    def read_hosts_file(self):
        """读取 hosts 文件内容"""
        with open(self.hosts_file, "r",encoding="utf-8") as file:
            return file.readlines()

    def write_hosts_file(self, content):
        """写入 hosts 文件内容"""
        with open(self.hosts_file, "w",encoding="utf-8") as file:
            file.writelines(content)

    def parse_hosts_file(self):
        """
        解析 hosts 文件，分离出程序控制部分和非程序控制部分
        更新点：将标记行包含在 program_section 中
        """
        lines = self.read_hosts_file()

        before = []
        program_section = []
        after = []
        
        section_found = False  # 是否已找到程序控制块
        in_program_section = False

        for line in lines:
            stripped_line = line.strip()
            
            # 检测到开始标记
            if stripped_line == self.BEGIN_MARKER:
                section_found = True
                in_program_section = True
                program_section.append(line)  # 将开始标记加入程序控制部分
            
            # 检测到结束标记
            elif stripped_line == self.END_MARKER:
                program_section.append(line)   # 将结束标记加入程序控制部分
                in_program_section = False
            
            # 处理程序控制部分的内容
            elif in_program_section:
                program_section.append(line)
            
            # 非程序控制部分
            else:
                if not section_found:
                    before.append(line)   # 程序控制块之前的内容
                else:
                    after.append(line)    # 程序控制块之后的内容

        return before, program_section, after

    def update_program_controlled_content(self, new_mappings):
        """
        更新程序控制部分的内容
        更新点：仅在存在映射时生成标记
        """
        before, _, after = self.parse_hosts_file()
        
        new_program_section = []
        if new_mappings:  # 仅当有映射时添加标记
            new_program_section.append(f"{self.BEGIN_MARKER}\n")
            for ip, hosts in new_mappings.items():
                new_program_section.append(f"{ip} {' '.join(hosts)}\n")
            new_program_section.append(f"{self.END_MARKER}\n")
        
        # 合并内容并写入文件
        self.write_hosts_file(before + new_program_section + after)

    def get_program_controlled_mappings(self):
        """
        获取程序控制部分的映射
        :return: 字典，格式为 {IP: [host1, host2, ...]}
        """
        _, program_section, _ = self.parse_hosts_file()
        mappings = {}

        for line in program_section:
            line = line.strip()
            if line and not line.startswith("#"):  # 忽略空行和注释
                parts = re.split(r'\s+', line)
                if len(parts) >= 2:
                    ip = parts[0]
                    hosts = parts[1:]
                    mappings[ip] = hosts

        return mappings

    

    def add_mapping(self, ip, hosts):
        """
        添加新的映射
        :param ip: IP 地址
        :param hosts: 主机名列表
        """
        mappings = self.get_program_controlled_mappings()
        if ip in mappings:
            existing_hosts = mappings[ip]
            new_hosts = [h for h in hosts if h not in existing_hosts]
            mappings[ip].extend(new_hosts)
        else:
            mappings[ip] = hosts
        self.update_program_controlled_content(mappings)

    def remove_mapping(self, ip, hosts=None):
        """
        删除映射
        :param ip: IP 地址
        :param hosts: 要删除的主机名列表（可选，如果为 None，则删除该 IP 的所有映射）
        """
        mappings = self.get_program_controlled_mappings()
        if ip in mappings:
            if hosts is None:
                del mappings[ip]
            else:
                mappings[ip] = [h for h in mappings[ip] if h not in hosts]
                if not mappings[ip]:
                    del mappings[ip]
        self.update_program_controlled_content(mappings)

    def view_mappings(self):
        """
        查看程序控制部分的映射
        """
        mappings = self.get_program_controlled_mappings()
        for ip, hosts in mappings.items():
            print(f"{ip}: {', '.join(hosts)}")

    def find_ips_by_host(self, host):
            """
            根据域名查找所有关联的 IP
            :param host: 要搜索的域名（如 "custom.host"）
            :return: 包含该域名的 IP 列表
            """
            mappings = self.get_program_controlled_mappings()
            ips = []
            for ip, hosts in mappings.items():
                if host in hosts:
                    ips.append(ip)
            return ips

    def remove_mappings_by_host(self, host):
        """
        通过域名删除所有关联 IP 的完整映射
        （直接删除包含该域名的所有 IP 条目）
        """
        ips = self.find_ips_by_host(host)
        for ip in ips:
            self.remove_mapping(ip)  # 调用原有方法删除整个 IP 条目

    def remove_single_host(self, host):
        """
        仅删除域名本身（保留同一 IP 下的其他域名）
        """
        mappings = self.get_program_controlled_mappings()
        updated = False

        # 遍历所有 IP 的域名列表
        for ip in list(mappings.keys()):  # 转换为列表避免字典修改异常
            if host in mappings[ip]:
                mappings[ip].remove(host)
                updated = True
                if not mappings[ip]:  # 如果该 IP 无其他域名则删除整个 IP
                    del mappings[ip]

        if updated:
            self.update_program_controlled_content(mappings)