from PyInstaller.utils.hooks import collect_all,collect_submodules
import os
datas = [('./res/resdata_rc.py', '.')]
if os.path.exists('./example/version.py'):
    datas.append(('./version.py', '.'))
binaries = []
hiddenimports = []
excludedimports = []
tmp_ret = collect_all('FluentUI')
print(tmp_ret)
