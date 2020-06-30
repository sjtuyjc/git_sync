#username of gerrit
user = 'admin'
#localhost of gerrit website
localhost = '192.168.0.210:29418/'
#names of all repos
module_list = ['dlc_fullchip', 'dlc_core', 'dlc_pgx', 'dlc_xys', 'dlc_nws', 'dlc_fxc', 'dlc_htt', 'dlc_klm', 'dlc_kts', 'dlc_lyp', 'dlc_pad']
#dir name of corresponding repo
dic = {'dlc_fullchip': 'fullchip', 'dlc_core': 'core', 'dlc_pgx': 'pgx', 'dlc_xys': 'xys', 'dlc_nws': 'nws', 'dlc_fxc': 'fxc', 'dlc_htt': 'htt', 'dlc_klm': 'klm', 'dlc_kts': 'kts', 'dlc_lyp': '', 'dlc_pad': ''}
#dirs that may be changed after csr files are regenerated and need to be recovered
dir_recover = ['tools', 'verif/uvcs']
#dirs need to be sync and merge
#dir_to_sync = ['common']
dir_to_sync = ['common', 'tools', 'verif/uvcs']
#should not be changed
module_wkspc = []
file_wkspc = {}
