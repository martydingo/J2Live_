rm -rf build dist
nicegui-pack --onefile --name "J2Live" --windowed src/j2live.py --osx-bundle-identifier 'dingo.j2live' --icon j2live.icns
cp -r venv/lib/python3.12/site-packages/ansible dist/J2Live.app/Contents/Frameworks/ansible
cp -r venv/lib/python3.12/site-packages/ansible dist/J2Live/_internal/ansible
