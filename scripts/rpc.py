#!/usr/bin/env python

from rpc.client import print_dict

import argparse
import rpc

try:
    from shlex import quote
except ImportError:
    from pipes import quote


def print_array(a):
    print(" ".join((quote(v) for v in a)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='SPDK RPC command line interface')
    parser.add_argument('-s', dest='server_addr',
                        help='RPC server address', default='/var/tmp/spdk.sock')
    parser.add_argument('-p', dest='port',
                        help='RPC port number (if server_addr is IP address)',
                        default=5260, type=int)
    parser.add_argument('-t', dest='timeout',
                        help='Timout as a floating point number expressed in seconds waiting for reponse. Default: 60.0',
                        default=60.0, type=float)
    parser.add_argument('-v', dest='verbose',
                        help='Verbose mode', action='store_true')
    subparsers = parser.add_subparsers(help='RPC methods')

    def get_rpc_methods(args):
        print_dict(rpc.get_rpc_methods(args))

    p = subparsers.add_parser('get_rpc_methods', help='Get list of supported RPC methods')
    p.set_defaults(func=get_rpc_methods)

    def save_config(args):
        rpc.save_config(args)

    p = subparsers.add_parser('save_config', help="""Write current (live) configuration of SPDK subsystems and targets.
    If no filename is given write configuration to stdout.""")
    p.add_argument('-f', '--filename', help="""File where to save JSON configuration to.""")
    p.add_argument('-i', '--indent', help="""Indent level. Value less than 0 mean compact mode. If filename is not given default
    indent level is 2. If writing to file of filename is '-' then default is compact mode.""", type=int, default=2)
    p.set_defaults(func=save_config)

    def load_config(args):
        rpc.load_config(args)

    p = subparsers.add_parser('load_config', help="""Configure SPDK subsystems and tagets using JSON RPC. If no file is
    provided or file is '-' read configuration from stdin.""")
    p.add_argument('--filename', help="""JSON Configuration file.""")
    p.set_defaults(func=load_config)

    # app
    def kill_instance(args):
        rpc.app.kill_instance(args)

    p = subparsers.add_parser('kill_instance', help='Send signal to instance')
    p.add_argument('sig_name', help='signal will be sent to server.')
    p.set_defaults(func=kill_instance)

    def context_switch_monitor(args):
        print_dict(rpc.app.context_switch_monitor(args))

    p = subparsers.add_parser('context_switch_monitor', help='Control whether the context switch monitor is enabled')
    p.add_argument('-e', '--enable', action='store_true', help='Enable context switch monitoring')
    p.add_argument('-d', '--disable', action='store_true', help='Disable context switch monitoring')
    p.set_defaults(func=context_switch_monitor)

    # bdev
    def construct_malloc_bdev(args):
        print_array(rpc.bdev.construct_malloc_bdev(args))

    p = subparsers.add_parser('construct_malloc_bdev',
                              help='Add a bdev with malloc backend')
    p.add_argument('-b', '--name', help="Name of the bdev")
    p.add_argument('-u', '--uuid', help="UUID of the bdev")
    p.add_argument(
        'total_size', help='Size of malloc bdev in MB (int > 0)', type=int)
    p.add_argument('block_size', help='Block size for this bdev', type=int)
    p.set_defaults(func=construct_malloc_bdev)

    def construct_null_bdev(args):
        print_array(rpc.bdev.construct_null_bdev(args))

    p = subparsers.add_parser('construct_null_bdev',
                              help='Add a bdev with null backend')
    p.add_argument('name', help='Block device name')
    p.add_argument('-u', '--uuid', help='UUID of the bdev')
    p.add_argument(
        'total_size', help='Size of null bdev in MB (int > 0)', type=int)
    p.add_argument('block_size', help='Block size for this bdev', type=int)
    p.set_defaults(func=construct_null_bdev)

    def construct_aio_bdev(args):
        print_array(rpc.bdev.construct_aio_bdev(args))

    p = subparsers.add_parser('construct_aio_bdev',
                              help='Add a bdev with aio backend')
    p.add_argument('filename', help='Path to device or file (ex: /dev/sda)')
    p.add_argument('name', help='Block device name')
    p.add_argument('block_size', help='Block size for this bdev', type=int, default=argparse.SUPPRESS)
    p.set_defaults(func=construct_aio_bdev)

    def construct_nvme_bdev(args):
        print_array(rpc.bdev.construct_nvme_bdev(args))

    p = subparsers.add_parser('construct_nvme_bdev',
                              help='Add bdev with nvme backend')
    p.add_argument('-b', '--name', help="Name of the bdev", required=True)
    p.add_argument('-t', '--trtype',
                   help='NVMe-oF target trtype: e.g., rdma, pcie', required=True)
    p.add_argument('-a', '--traddr',
                   help='NVMe-oF target address: e.g., an ip address or BDF', required=True)
    p.add_argument('-f', '--adrfam',
                   help='NVMe-oF target adrfam: e.g., ipv4, ipv6, ib, fc, intra_host')
    p.add_argument('-s', '--trsvcid',
                   help='NVMe-oF target trsvcid: e.g., a port number')
    p.add_argument('-n', '--subnqn', help='NVMe-oF target subnqn')
    p.set_defaults(func=construct_nvme_bdev)

    def construct_rbd_bdev(args):
        print_array(rpc.bdev.construct_rbd_bdev(args))

    p = subparsers.add_parser('construct_rbd_bdev',
                              help='Add a bdev with ceph rbd backend')
    p.add_argument('-b', '--name', help="Name of the bdev", required=False)
    p.add_argument('pool_name', help='rbd pool name')
    p.add_argument('rbd_name', help='rbd image name')
    p.add_argument('block_size', help='rbd block size', type=int)
    p.set_defaults(func=construct_rbd_bdev)

    def construct_error_bdev(args):
        rpc.bdev.construct_error_bdev(args)

    p = subparsers.add_parser('construct_error_bdev',
                              help='Add bdev with error injection backend')
    p.add_argument('base_name', help='base bdev name')
    p.set_defaults(func=construct_error_bdev)

    def construct_pmem_bdev(args):
        print_array(rpc.bdev.construct_pmem_bdev(args))

    p = subparsers.add_parser('construct_pmem_bdev', help='Add a bdev with pmem backend')
    p.add_argument('pmem_file', help='Path to pmemblk pool file')
    p.add_argument('-n', '--name', help='Block device name', required=True)
    p.set_defaults(func=construct_pmem_bdev)

    def get_bdevs(args):
        print_dict(rpc.bdev.get_bdevs(args))

    p = subparsers.add_parser(
        'get_bdevs', help='Display current blockdev list or required blockdev')
    p.add_argument('-b', '--name', help="Name of the Blockdev. Example: Nvme0n1", required=False)
    p.set_defaults(func=get_bdevs)

    def delete_bdev(args):
        rpc.bdev.delete_bdev(args)

    def get_bdevs_config(args):
        print_dict(rpc.bdev.get_bdevs_config(args))

    p = subparsers.add_parser(
        'get_bdevs_config', help='Display current (live) blockdev configuration list or required blockdev')
    p.add_argument('-b', '--name', help="Name of the Blockdev. Example: Nvme0n1", required=False)
    p.set_defaults(func=get_bdevs_config)

    p = subparsers.add_parser('delete_bdev', help='Delete a blockdev')
    p.add_argument(
        'bdev_name', help='Blockdev name to be deleted. Example: Malloc0.')
    p.set_defaults(func=delete_bdev)

    def bdev_inject_error(args):
        rpc.bdev.bdev_inject_error(args)

    p = subparsers.add_parser('bdev_inject_error', help='bdev inject error')
    p.add_argument('name', help="""the name of the error injection bdev""")
    p.add_argument('io_type', help="""io_type: 'clear' 'read' 'write' 'unmap' 'flush' 'all'""")
    p.add_argument('error_type', help="""error_type: 'failure' 'pending'""")
    p.add_argument(
        '-n', '--num', help='the number of commands you want to fail', type=int, default=1)
    p.set_defaults(func=bdev_inject_error)

    def apply_firmware(args):
        print_dict(rpc.bdev.apply_firmware(args))

    p = subparsers.add_parser('apply_firmware', help='Download and commit firmware to NVMe device')
    p.add_argument('filename', help='filename of the firmware to download')
    p.add_argument('bdev_name', help='name of the NVMe device')
    p.set_defaults(func=apply_firmware)

    # iSCSI
    def get_portal_groups(args):
        print_dict(rpc.iscsi.get_portal_groups(args))

    p = subparsers.add_parser(
        'get_portal_groups', help='Display current portal group configuration')
    p.set_defaults(func=get_portal_groups)

    def get_initiator_groups(args):
        print_dict(rpc.iscsi.get_initiator_groups(args))

    p = subparsers.add_parser('get_initiator_groups',
                              help='Display current initiator group configuration')
    p.set_defaults(func=get_initiator_groups)

    def get_target_nodes(args):
        print_dict(rpc.iscsi.get_target_nodes(args))

    p = subparsers.add_parser('get_target_nodes', help='Display target nodes')
    p.set_defaults(func=get_target_nodes)

    def construct_target_node(args):
        rpc.iscsi.construct_target_node(args)

    p = subparsers.add_parser('construct_target_node',
                              help='Add a target node')
    p.add_argument('name', help='Target node name (ASCII)')
    p.add_argument('alias_name', help='Target node alias name (ASCII)')
    p.add_argument('bdev_name_id_pairs', help="""Whitespace-separated list of <bdev name:LUN ID> pairs enclosed
    in quotes.  Format:  'bdev_name0:id0 bdev_name1:id1' etc
    Example: 'Malloc0:0 Malloc1:1 Malloc5:2'
    *** The bdevs must pre-exist ***
    *** LUN0 (id = 0) is required ***
    *** bdevs names cannot contain space or colon characters ***""")
    p.add_argument('pg_ig_mappings', help="""List of (Portal_Group_Tag:Initiator_Group_Tag) mappings
    Whitespace separated, quoted, mapping defined with colon
    separated list of "tags" (int > 0)
    Example: '1:1 2:2 2:1'
    *** The Portal/Initiator Groups must be precreated ***""")
    p.add_argument('queue_depth', help='Desired target queue depth', type=int)
    p.add_argument('-g', '--chap-group', help="""Authentication group ID for this target node.
    *** Authentication group must be precreated ***""", type=int, default=0)
    p.add_argument('-d', '--disable-chap', help="""CHAP authentication should be disabled for this target node.
    *** Mutually exclusive with --require-chap ***""", action='store_true')
    p.add_argument('-r', '--require-chap', help="""CHAP authentication should be required for this target node.
    *** Mutually exclusive with --disable-chap ***""", action='store_true')
    p.add_argument(
        '-m', '--mutual-chap', help='CHAP authentication should be mutual/bidirectional.', action='store_true')
    p.add_argument('-H', '--header-digest',
                   help='Header Digest should be required for this target node.', action='store_true')
    p.add_argument('-D', '--data-digest',
                   help='Data Digest should be required for this target node.', action='store_true')
    p.set_defaults(func=construct_target_node)

    def target_node_add_lun(args):
        rpc.iscsi.target_node_add_lun(args)

    p = subparsers.add_parser('target_node_add_lun', help='Add LUN to the target node')
    p.add_argument('name', help='Target node name (ASCII)')
    p.add_argument('bdev_name', help="""bdev name enclosed in quotes.
    *** bdev name cannot contain space or colon characters ***""")
    p.add_argument('-i', dest='lun_id', help="""LUN ID (integer >= 0)
    *** If LUN ID is omitted or -1, the lowest free one is assigned ***""", type=int, required=False)
    p.set_defaults(func=target_node_add_lun)

    def add_pg_ig_maps(args):
        rpc.iscsi.add_pg_ig_maps(args)

    p = subparsers.add_parser('add_pg_ig_maps', help='Add PG-IG maps to the target node')
    p.add_argument('name', help='Target node name (ASCII)')
    p.add_argument('pg_ig_mappings', help="""List of (Portal_Group_Tag:Initiator_Group_Tag) mappings
    Whitespace separated, quoted, mapping defined with colon
    separated list of "tags" (int > 0)
    Example: '1:1 2:2 2:1'
    *** The Portal/Initiator Groups must be precreated ***""")
    p.set_defaults(func=add_pg_ig_maps)

    def delete_pg_ig_maps(args):
        rpc.iscsi.delete_pg_ig_maps(args)

    p = subparsers.add_parser('delete_pg_ig_maps', help='Delete PG-IG maps from the target node')
    p.add_argument('name', help='Target node name (ASCII)')
    p.add_argument('pg_ig_mappings', help="""List of (Portal_Group_Tag:Initiator_Group_Tag) mappings
    Whitespace separated, quoted, mapping defined with colon
    separated list of "tags" (int > 0)
    Example: '1:1 2:2 2:1'
    *** The Portal/Initiator Groups must be precreated ***""")
    p.set_defaults(func=delete_pg_ig_maps)

    def add_portal_group(args):
        rpc.iscsi.add_portal_group(args)

    p = subparsers.add_parser('add_portal_group', help='Add a portal group')
    p.add_argument(
        'tag', help='Portal group tag (unique, integer > 0)', type=int)
    p.add_argument('portal_list', nargs=argparse.REMAINDER, help="""List of portals in 'host:port@cpumask' format, separated by whitespace
    (cpumask is optional and can be skipped)
    Example: '192.168.100.100:3260' '192.168.100.100:3261' '192.168.100.100:3262@0x1""")
    p.set_defaults(func=add_portal_group)

    def add_initiator_group(args):
        rpc.iscsi.add_initiator_group(args)

    p = subparsers.add_parser('add_initiator_group',
                              help='Add an initiator group')
    p.add_argument(
        'tag', help='Initiator group tag (unique, integer > 0)', type=int)
    p.add_argument('initiator_list', help="""Whitespace-separated list of initiator hostnames or IP addresses,
    enclosed in quotes.  Example: 'ANY' or '127.0.0.1 192.168.200.100'""")
    p.add_argument('netmask_list', help="""Whitespace-separated list of initiator netmasks enclosed in quotes.
    Example: '255.255.0.0 255.248.0.0' etc""")
    p.set_defaults(func=add_initiator_group)

    def add_initiators_to_initiator_group(args):
        rpc.iscsi.add_initiators_to_initiator_group(args)

    p = subparsers.add_parser('add_initiators_to_initiator_group',
                              help='Add initiators to an existing initiator group')
    p.add_argument(
        'tag', help='Initiator group tag (unique, integer > 0)', type=int)
    p.add_argument('-n', dest='initiator_list', help="""Whitespace-separated list of initiator hostnames or IP addresses,
    enclosed in quotes.  This parameter can be omitted.  Example: 'ANY' or '127.0.0.1 192.168.200.100'""", required=False)
    p.add_argument('-m', dest='netmask_list', help="""Whitespace-separated list of initiator netmasks enclosed in quotes.
    This parameter can be omitted.  Example: '255.255.0.0 255.248.0.0' etc""", required=False)
    p.set_defaults(func=add_initiators_to_initiator_group)

    def delete_initiators_from_initiator_group(args):
        rpc.iscsi.delete_initiators_from_initiator_group(args)

    p = subparsers.add_parser('delete_initiators_from_initiator_group',
                              help='Delete initiators from an existing initiator group')
    p.add_argument(
        'tag', help='Initiator group tag (unique, integer > 0)', type=int)
    p.add_argument('-n', dest='initiator_list', help="""Whitespace-separated list of initiator hostnames or IP addresses,
    enclosed in quotes.  This parameter can be omitted.  Example: 'ANY' or '127.0.0.1 192.168.200.100'""", required=False)
    p.add_argument('-m', dest='netmask_list', help="""Whitespace-separated list of initiator netmasks enclosed in quotes.
    This parameter can be omitted.  Example: '255.255.0.0 255.248.0.0' etc""", required=False)
    p.set_defaults(func=delete_initiators_from_initiator_group)

    def delete_target_node(args):
        rpc.iscsi.delete_target_node(args)

    p = subparsers.add_parser('delete_target_node',
                              help='Delete a target node')
    p.add_argument('target_node_name',
                   help='Target node name to be deleted. Example: iqn.2016-06.io.spdk:disk1.')
    p.set_defaults(func=delete_target_node)

    def delete_portal_group(args):
        rpc.iscsi.delete_portal_group(args)

    p = subparsers.add_parser('delete_portal_group',
                              help='Delete a portal group')
    p.add_argument(
        'tag', help='Portal group tag (unique, integer > 0)', type=int)
    p.set_defaults(func=delete_portal_group)

    def delete_initiator_group(args):
        rpc.iscsi.delete_initiator_group(args)

    p = subparsers.add_parser('delete_initiator_group',
                              help='Delete an initiator group')
    p.add_argument(
        'tag', help='Initiator group tag (unique, integer > 0)', type=int)
    p.set_defaults(func=delete_initiator_group)

    def get_iscsi_connections(args):
        print_dict(rpc.iscsi.get_iscsi_connections(args))

    p = subparsers.add_parser('get_iscsi_connections',
                              help='Display iSCSI connections')
    p.set_defaults(func=get_iscsi_connections)

    def get_iscsi_global_params(args):
        print_dict(rpc.iscsi.get_iscsi_global_params(args))

    p = subparsers.add_parser('get_iscsi_global_params', help='Display iSCSI global parameters')
    p.set_defaults(func=get_iscsi_global_params)

    def get_scsi_devices(args):
        print_dict(rpc.iscsi.get_scsi_devices(args))

    p = subparsers.add_parser('get_scsi_devices', help='Display SCSI devices')
    p.set_defaults(func=get_scsi_devices)

    # log
    def set_trace_flag(args):
        rpc.log.set_trace_flag(args)

    p = subparsers.add_parser('set_trace_flag', help='set trace flag')
    p.add_argument(
        'flag', help='trace mask we want to set. (for example "debug").')
    p.set_defaults(func=set_trace_flag)

    def clear_trace_flag(args):
        rpc.log.clear_trace_flag(args)

    p = subparsers.add_parser('clear_trace_flag', help='clear trace flag')
    p.add_argument(
        'flag', help='trace mask we want to clear. (for example "debug").')
    p.set_defaults(func=clear_trace_flag)

    def get_trace_flags(args):
        print_dict(rpc.log.get_trace_flags(args))

    p = subparsers.add_parser('get_trace_flags', help='get trace flags')
    p.set_defaults(func=get_trace_flags)

    def set_log_level(args):
        rpc.log.set_log_level(args)

    p = subparsers.add_parser('set_log_level', help='set log level')
    p.add_argument('level', help='log level we want to set. (for example "DEBUG").')
    p.set_defaults(func=set_log_level)

    def get_log_level(args):
        print_dict(rpc.log.get_log_level(args))

    p = subparsers.add_parser('get_log_level', help='get log level')
    p.set_defaults(func=get_log_level)

    def set_log_print_level(args):
        rpc.log.set_log_print_level(args)

    p = subparsers.add_parser('set_log_print_level', help='set log print level')
    p.add_argument('level', help='log print level we want to set. (for example "DEBUG").')
    p.set_defaults(func=set_log_print_level)

    def get_log_print_level(args):
        print_dict(rpc.log.get_log_print_level(args))

    p = subparsers.add_parser('get_log_print_level', help='get log print level')
    p.set_defaults(func=get_log_print_level)

    # lvol
    def construct_lvol_store(args):
        print_array(rpc.lvol.construct_lvol_store(args))

    p = subparsers.add_parser('construct_lvol_store', help='Add logical volume store on base bdev')
    p.add_argument('bdev_name', help='base bdev name')
    p.add_argument('lvs_name', help='name for lvol store')
    p.add_argument('-c', '--cluster-sz', help='size of cluster (in bytes)', type=int, required=False)
    p.set_defaults(func=construct_lvol_store)

    def rename_lvol_store(args):
        rpc.lvol.rename_lvol_store(args)

    p = subparsers.add_parser('rename_lvol_store', help='Change logical volume store name')
    p.add_argument('old_name', help='old name')
    p.add_argument('new_name', help='new name')
    p.set_defaults(func=rename_lvol_store)

    def construct_lvol_bdev(args):
        print_array(rpc.lvol.construct_lvol_bdev(args))

    p = subparsers.add_parser('construct_lvol_bdev', help='Add a bdev with an logical volume backend')
    p.add_argument('-u', '--uuid', help='lvol store UUID', required=False)
    p.add_argument('-l', '--lvs_name', help='lvol store name', required=False)
    p.add_argument('-t', '--thin-provision', action='store_true', help='create lvol bdev as thin provisioned')
    p.add_argument('lvol_name', help='name for this lvol')
    p.add_argument('size', help='size in MiB for this bdev', type=int)
    p.set_defaults(func=construct_lvol_bdev)

    def rename_lvol_bdev(args):
        rpc.lvol.rename_lvol_bdev(args)

    p = subparsers.add_parser('rename_lvol_bdev', help='Change lvol bdev name')
    p.add_argument('old_name', help='lvol bdev name')
    p.add_argument('new_name', help='new lvol name')
    p.set_defaults(func=rename_lvol_bdev)

    # Logical volume resize feature is disabled, as it is currently work in progress
    # def resize_lvol_bdev(args):
    #     rpc.lvol.resize_bdev(args)
    #
    # p = subparsers.add_parser('resize_lvol_bdev', help='Resize existing lvol bdev')
    # p.add_argument('name', help='lvol bdev name')
    # p.add_argument('size', help='new size in MiB for this bdev', type=int)
    # p.set_defaults(func=resize_lvol_bdev)

    def destroy_lvol_store(args):
        rpc.lvol.destroy_lvol_store(args)

    p = subparsers.add_parser('destroy_lvol_store', help='Destroy an logical volume store')
    p.add_argument('-u', '--uuid', help='lvol store UUID', required=False)
    p.add_argument('-l', '--lvs_name', help='lvol store name', required=False)
    p.set_defaults(func=destroy_lvol_store)

    def get_lvol_stores(args):
        print_dict(rpc.lvol.get_lvol_stores(args))

    p = subparsers.add_parser('get_lvol_stores', help='Display current logical volume store list')
    p.add_argument('-u', '--uuid', help='lvol store UUID', required=False)
    p.add_argument('-l', '--lvs_name', help='lvol store name', required=False)
    p.set_defaults(func=get_lvol_stores)

    # nbd
    def start_nbd_disk(args):
        rpc.nbd.start_nbd_disk(args)

    p = subparsers.add_parser('start_nbd_disk', help='Export a bdev as a nbd disk')
    p.add_argument('bdev_name', help='Blockdev name to be exported. Example: Malloc0.')
    p.add_argument('nbd_device', help='Nbd device name to be assigned. Example: /dev/nbd0.')
    p.set_defaults(func=start_nbd_disk)

    def stop_nbd_disk(args):
        rpc.nbd.stop_nbd_disk(args)

    p = subparsers.add_parser('stop_nbd_disk', help='Stop a nbd disk')
    p.add_argument('nbd_device', help='Nbd device name to be stopped. Example: /dev/nbd0.')
    p.set_defaults(func=stop_nbd_disk)

    def get_nbd_disks(args):
        print_dict(rpc.nbd.get_nbd_disks(args))

    p = subparsers.add_parser('get_nbd_disks', help='Display full or specified nbd device list')
    p.add_argument('-n', '--nbd_device', help="Path of the nbd device. Example: /dev/nbd0", required=False)
    p.set_defaults(func=get_nbd_disks)

    # net
    def add_ip_address(args):
        rpc.net.add_ip_address(args)

    p = subparsers.add_parser('add_ip_address', help='Add IP address')
    p.add_argument('ifc_index', help='ifc index of the nic device.', type=int)
    p.add_argument('ip_addr', help='ip address will be added.')
    p.set_defaults(func=add_ip_address)

    def delete_ip_address(args):
        rpc.net.delete_ip_address(args)

    p = subparsers.add_parser('delete_ip_address', help='Delete IP address')
    p.add_argument('ifc_index', help='ifc index of the nic device.', type=int)
    p.add_argument('ip_addr', help='ip address will be deleted.')
    p.set_defaults(func=delete_ip_address)

    def get_interfaces(args):
        print_dict(rpc.net.get_interfaces(args))

    p = subparsers.add_parser(
        'get_interfaces', help='Display current interface list')
    p.set_defaults(func=get_interfaces)

    # NVMe-oF
    def get_nvmf_subsystems(args):
        print_dict(rpc.nvmf.get_nvmf_subsystems(args))

    p = subparsers.add_parser('get_nvmf_subsystems',
                              help='Display nvmf subsystems')
    p.set_defaults(func=get_nvmf_subsystems)

    def construct_nvmf_subsystem(args):
        rpc.nvmf.construct_nvmf_subsystem(args)

    p = subparsers.add_parser('construct_nvmf_subsystem', help='Add a nvmf subsystem')
    p.add_argument('nqn', help='Target nqn(ASCII)')
    p.add_argument('listen', help="""comma-separated list of Listen <trtype:transport_name traddr:address trsvcid:port_id> pairs enclosed
    in quotes.  Format:  'trtype:transport0 traddr:traddr0 trsvcid:trsvcid0,trtype:transport1 traddr:traddr1 trsvcid:trsvcid1' etc
    Example: 'trtype:RDMA traddr:192.168.100.8 trsvcid:4420,trtype:RDMA traddr:192.168.100.9 trsvcid:4420'""")
    p.add_argument('hosts', help="""Whitespace-separated list of host nqn list.
    Format:  'nqn1 nqn2' etc
    Example: 'nqn.2016-06.io.spdk:init nqn.2016-07.io.spdk:init'""")
    p.add_argument("-a", "--allow-any-host", action='store_true', help="Allow any host to connect (don't enforce host NQN whitelist)")
    p.add_argument("-s", "--serial_number", help="""
    Format:  'sn' etc
    Example: 'SPDK00000000000001'""", default='0000:00:01.0')
    p.add_argument("-n", "--namespaces", help="""Whitespace-separated list of namespaces
    Format:  'bdev_name1[:nsid1] bdev_name2[:nsid2] bdev_name3[:nsid3]' etc
    Example: '1:Malloc0 2:Malloc1 3:Malloc2'
    *** The devices must pre-exist ***""")
    p.set_defaults(func=construct_nvmf_subsystem)

    def delete_nvmf_subsystem(args):
        rpc.nvmf.delete_nvmf_subsystem(args)

    p = subparsers.add_parser('delete_nvmf_subsystem',
                              help='Delete a nvmf subsystem')
    p.add_argument('subsystem_nqn',
                   help='subsystem nqn to be deleted. Example: nqn.2016-06.io.spdk:cnode1.')
    p.set_defaults(func=delete_nvmf_subsystem)

    def nvmf_subsystem_add_listener(args):
        rpc.nvmf.nvmf_subsystem_add_listener(args)

    p = subparsers.add_parser('nvmf_subsystem_add_listener', help='Add a listener to an NVMe-oF subsystem')
    p.add_argument('nqn', help='NVMe-oF subsystem NQN')
    p.add_argument('-t', '--trtype', help='NVMe-oF transport type: e.g., rdma', required=True)
    p.add_argument('-a', '--traddr', help='NVMe-oF transport address: e.g., an ip address', required=True)
    p.add_argument('-f', '--adrfam', help='NVMe-oF transport adrfam: e.g., ipv4, ipv6, ib, fc, intra_host')
    p.add_argument('-s', '--trsvcid', help='NVMe-oF transport service id: e.g., a port number')
    p.set_defaults(func=nvmf_subsystem_add_listener)

    def nvmf_subsystem_remove_listener(args):
        rpc.nvmf.nvmf_subsystem_remove_listener(args)

    p = subparsers.add_parser('nvmf_subsystem_remove_listener', help='Remove a listener from an NVMe-oF subsystem')
    p.add_argument('nqn', help='NVMe-oF subsystem NQN')
    p.add_argument('-t', '--trtype', help='NVMe-oF transport type: e.g., rdma', required=True)
    p.add_argument('-a', '--traddr', help='NVMe-oF transport address: e.g., an ip address', required=True)
    p.add_argument('-f', '--adrfam', help='NVMe-oF transport adrfam: e.g., ipv4, ipv6, ib, fc, intra_host')
    p.add_argument('-s', '--trsvcid', help='NVMe-oF transport service id: e.g., a port number')
    p.set_defaults(func=nvmf_subsystem_remove_listener)

    def nvmf_subsystem_add_ns(args):
        rpc.nvmf.nvmf_subsystem_add_ns(args)

    p = subparsers.add_parser('nvmf_subsystem_add_ns', help='Add a namespace to an NVMe-oF subsystem')
    p.add_argument('nqn', help='NVMe-oF subsystem NQN')
    p.add_argument('bdev_name', help='The name of the bdev that will back this namespace')
    p.add_argument('-n', '--nsid', help='The requested NSID (optional)', type=int)
    p.add_argument('-g', '--nguid', help='Namespace globally unique identifier (optional)')
    p.add_argument('-e', '--eui64', help='Namespace EUI-64 identifier (optional)')
    p.set_defaults(func=nvmf_subsystem_add_ns)

    def nvmf_subsystem_remove_ns(args):
        rpc.nvmf.nvmf_subsystem_remove_ns(args)

    p = subparsers.add_parser('nvmf_subsystem_remove_ns', help='Remove a namespace to an NVMe-oF subsystem')
    p.add_argument('nqn', help='NVMe-oF subsystem NQN')
    p.add_argument('nsid', help='The requested NSID', type=int)
    p.set_defaults(func=nvmf_subsystem_remove_ns)

    def nvmf_subsystem_add_host(args):
        rpc.nvmf.nvmf_subsystem_add_host(args)

    p = subparsers.add_parser('nvmf_subsystem_add_host', help='Add a host to an NVMe-oF subsystem')
    p.add_argument('nqn', help='NVMe-oF subsystem NQN')
    p.add_argument('host', help='Host NQN to allow')
    p.set_defaults(func=nvmf_subsystem_add_host)

    def nvmf_subsystem_remove_host(args):
        rpc.nvmf.nvmf_subsystem_remove_host(args)

    p = subparsers.add_parser('nvmf_subsystem_remove_host', help='Remove a host from an NVMe-oF subsystem')
    p.add_argument('nqn', help='NVMe-oF subsystem NQN')
    p.add_argument('host', help='Host NQN to remove')
    p.set_defaults(func=nvmf_subsystem_remove_host)

    def nvmf_subsystem_allow_any_host(args):
        rpc.nvmf.nvmf_subsystem_allow_any_host(args)

    p = subparsers.add_parser('nvmf_subsystem_allow_any_host', help='Allow any host to connect to the subsystem')
    p.add_argument('nqn', help='NVMe-oF subsystem NQN')
    p.add_argument('-e', '--enable', action='store_true', help='Enable allowing any host')
    p.add_argument('-d', '--disable', action='store_true', help='Disable allowing any host')
    p.set_defaults(func=nvmf_subsystem_allow_any_host)

    # pmem
    def create_pmem_pool(args):
        rpc.pmem.create_pmem_pool(args)

    p = subparsers.add_parser('create_pmem_pool', help='Create pmem pool')
    p.add_argument('pmem_file', help='Path to pmemblk pool file')
    p.add_argument('total_size', help='Size of malloc bdev in MB (int > 0)', type=int)
    p.add_argument('block_size', help='Block size for this pmem pool', type=int)
    p.set_defaults(func=create_pmem_pool)

    def pmem_pool_info(args):
        print_dict(rpc.pmem.pmem_pool_info(args))

    p = subparsers.add_parser('pmem_pool_info', help='Display pmem pool info and check consistency')
    p.add_argument('pmem_file', help='Path to pmemblk pool file')
    p.set_defaults(func=pmem_pool_info)

    def delete_pmem_pool(args):
        rpc.pmem.delete_pmem_pool(args)

    p = subparsers.add_parser('delete_pmem_pool', help='Delete pmem pool')
    p.add_argument('pmem_file', help='Path to pmemblk pool file')
    p.set_defaults(func=delete_pmem_pool)

    # subsystem
    def get_subsystems(args):
        print_dict(rpc.subsystem.get_subsystems(args))

    p = subparsers.add_parser('get_subsystems', help=""""Print subsystems array in initialization order. Each subsystem
    entry contain (unsorted) array of subsystems it depends on.""")
    p.set_defaults(func=get_subsystems)

    def get_subsystem_config(args):
        print_dict(rpc.subsystem.get_subsystem_config(args))

    p = subparsers.add_parser('get_subsystem_config', help=""""Print subsystem configuration""")
    p.add_argument('name', help='Name of subsystem to query')
    p.set_defaults(func=get_subsystem_config)

    # vhost
    def set_vhost_controller_coalescing(args):
        rpc.vhost.set_vhost_controller_coalescing(args)

    p = subparsers.add_parser('set_vhost_controller_coalescing', help='Set vhost controller coalescing')
    p.add_argument('ctrlr', help='controller name')
    p.add_argument('delay_base_us', help='Base delay time', type=int)
    p.add_argument('iops_threshold', help='IOPS threshold when coalescing is enabled', type=int)
    p.set_defaults(func=set_vhost_controller_coalescing)

    def construct_vhost_scsi_controller(args):
        rpc.vhost.construct_vhost_scsi_controller(args)

    p = subparsers.add_parser(
        'construct_vhost_scsi_controller', help='Add new vhost controller')
    p.add_argument('ctrlr', help='controller name')
    p.add_argument('--cpumask', help='cpu mask for this controller')
    p.set_defaults(func=construct_vhost_scsi_controller)

    def add_vhost_scsi_lun(args):
        rpc.vhost.add_vhost_scsi_lun(args)

    p = subparsers.add_parser('add_vhost_scsi_lun',
                              help='Add lun to vhost controller')
    p.add_argument('ctrlr', help='conntroller name where add lun')
    p.add_argument('scsi_target_num', help='scsi_target_num', type=int)
    p.add_argument('bdev_name', help='bdev name')
    p.set_defaults(func=add_vhost_scsi_lun)

    def remove_vhost_scsi_target(args):
        rpc.vhost.remove_vhost_scsi_target(args)

    p = subparsers.add_parser('remove_vhost_scsi_target', help='Remove target from vhost controller')
    p.add_argument('ctrlr', help='controller name to remove target from')
    p.add_argument('scsi_target_num', help='scsi_target_num', type=int)
    p.set_defaults(func=remove_vhost_scsi_target)

    def construct_vhost_blk_controller(args):
        rpc.vhost.construct_vhost_blk_controller(args)

    p = subparsers.add_parser('construct_vhost_blk_controller', help='Add a new vhost block controller')
    p.add_argument('ctrlr', help='controller name')
    p.add_argument('dev_name', help='device name')
    p.add_argument('--cpumask', help='cpu mask for this controller')
    p.add_argument("-r", "--readonly", action='store_true', help='Set controller as read-only')
    p.set_defaults(func=construct_vhost_blk_controller)

    def get_vhost_controllers(args):
        print_dict(rpc.vhost.get_vhost_controllers(args))

    p = subparsers.add_parser('get_vhost_controllers', help='List vhost controllers')
    p.set_defaults(func=get_vhost_controllers)

    def remove_vhost_controller(args):
        rpc.vhost.remove_vhost_controller(args)

    p = subparsers.add_parser('remove_vhost_controller', help='Remove a vhost controller')
    p.add_argument('ctrlr', help='controller name')
    p.set_defaults(func=remove_vhost_controller)

    def construct_virtio_user_scsi_bdev(args):
        print_dict(rpc.vhost.construct_virtio_user_scsi_bdev(args))

    p = subparsers.add_parser('construct_virtio_user_scsi_bdev', help="""Connect to virtio user scsi device.
    This imply scan and add bdevs offered by remote side.
    Result is array of added bdevs.""")
    p.add_argument('path', help='Path to Virtio SCSI socket')
    p.add_argument('name', help="""Use this name as base instead of 'VirtioScsiN'
    Base will be used to construct new bdev's found on target by adding 't<TARGET_ID>' sufix.""")
    p.add_argument('--vq-count', help='Number of virtual queues to be used.', type=int)
    p.add_argument('--vq-size', help='Size of each queue', type=int)
    p.set_defaults(func=construct_virtio_user_scsi_bdev)

    def construct_virtio_pci_scsi_bdev(args):
        print_dict(rpc.vhost.construct_virtio_pci_scsi_bdev(args))

    p = subparsers.add_parser('construct_virtio_pci_scsi_bdev', help="""Create a Virtio
    SCSI device from a virtio-pci device.""")
    p.add_argument('pci_address', help="""PCI address in domain:bus:device.function format or
    domain.bus.device.function format""")
    p.add_argument('name', help="""Name for the virtio device.
    It will be inhereted by all created bdevs, which are named n the following format: <name>t<target_id>""")
    p.set_defaults(func=construct_virtio_pci_scsi_bdev)

    def remove_virtio_scsi_bdev(args):
        rpc.vhost.remove_virtio_scsi_bdev(args)

    p = subparsers.add_parser('remove_virtio_scsi_bdev', help="""Remove a Virtio-SCSI device
    This will delete all bdevs exposed by this device""")
    p.add_argument('name', help='Virtio device name. E.g. VirtioUser0')
    p.set_defaults(func=remove_virtio_scsi_bdev)

    def construct_virtio_user_blk_bdev(args):
        print_dict(rpc.vhost.construct_virtio_user_blk_bdev(args))

    p = subparsers.add_parser('construct_virtio_user_blk_bdev', help='Connect to a virtio user blk device.')
    p.add_argument('path', help='Path to Virtio BLK socket')
    p.add_argument('name', help='Name for the bdev')
    p.add_argument('--vq-count', help='Number of virtual queues to be used.', type=int)
    p.add_argument('--vq-size', help='Size of each queue', type=int)
    p.set_defaults(func=construct_virtio_user_blk_bdev)

    def construct_virtio_pci_blk_bdev(args):
        print_dict(rpc.vhost.construct_virtio_pci_blk_bdev(args))

    p = subparsers.add_parser('construct_virtio_pci_blk_bdev', help='Create a Virtio Blk device from a virtio-pci device.')
    p.add_argument('pci_address', help="""PCI address in domain:bus:device.function format or
    domain.bus.device.function format""")
    p.add_argument('name', help='Name for the bdev')
    p.set_defaults(func=construct_virtio_pci_blk_bdev)

    args = parser.parse_args()

    args.client = rpc.client.JSONRPCClient(args.server_addr, args.port, args.verbose, args.timeout)
    args.func(args)
