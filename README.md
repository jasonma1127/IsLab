# IsLab

# Tools

## Radare2

```
sudo apt-get update -y
sudo apt-get install -y radare2
```

## UPX

```
sudo apt-get update -y
sudo apt-get install -y upx
```

## Detect It Easy (DIE)

```
sudo apt update
sudo apt install git qtbase5-dev qtscript5-dev qttools5-dev-tools git build-essential qtchooser
git clone --recursive https://github.com/horsicq/DIE-engine
cd DIE-engine
bash -x build_dpkg.sh
sudo dpkg -i release/die_*.deb
```
