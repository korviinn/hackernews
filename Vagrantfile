# -*- mode: ruby -*-
# vi: set ft=ruby :

$project_name = "python-hackernews"

$provision_script = <<-SCRIPT
DEV_USER=ubuntu

echo "*** Starting VM (dev user '${DEV_USER}') ***"

echo "==> 1. Installing required packages..."

add-apt-repository -y ppa:deadsnakes/ppa
apt-get update
apt-get install -y python3.7-dev python3-pip git
python3.7 -m pip install pipenv

git config --global user.name  "Kribesk"
git config --global user.email "kribesk@gmail.com"


echo "==> 2. Preparing python environment..."

su - ${DEV_USER} -c 'cd /python-hackernews && make venv'


echo "==> 3. Installing PyCharm 2018.2..."

apt-get install -y xterm libxtst6 libxi6 libxrender1
mkdir -p /opt/pycharm
chown ${DEV_USER}:${DEV_USER} /opt/pycharm

cd /media
if [[ ! -f pycharm-professional-2018.2.tar.gz ]]; then
  wget https://download.jetbrains.com/python/pycharm-professional-2018.2.tar.gz
fi

tar -xf /media/pycharm-professional-2018.2.tar.gz -C /opt/pycharm --strip-components=1


SCRIPT


Vagrant.configure("2") do |config|

    config.vm.define $project_name do |s|
      s.vm.box = "ubuntu/xenial64"
      s.vm.hostname = $project_name
      s.vm.box_check_update = false

      s.vm.provider "virtualbox" do |vb|
        vb.name = $project_name
        vb.memory = "4096"
        vb.cpus = 4
      end

      s.vm.network "forwarded_port", guest: 8888, host: 8888

      s.vm.synced_folder ".", "/vagrant", disabled: true
      s.vm.synced_folder ".", "/" + $project_name, type: "virtualbox"
      s.vm.synced_folder "D:\\Media\\soft-linux", "/media", type: "virtualbox"

      s.vm.provision "shell", inline: $provision_script
    end

end
