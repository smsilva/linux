alias aac='az account show --output jsonc'
alias aal='az account list --output table'
alias aas='$(azure-account-selection); export ARM_SAS_TOKEN=$(cat ${HOME}/.credentials/azure/${ARM_STORAGE_ACCOUNT_NAME}.sas-token) && arm'
alias acrl='az acr list --output table'
alias aglp='agl | grep -E "Name|azure-.*|sample|dummy|^wasp|^be.*platform-c|^be.*platform-a"'
alias aksl='az aks list --output table'
alias anagl='az network application-gateway list -o table'
alias anl='az network vnet list -o table'
alias armd=". armd && arm"
alias c='clear'
alias cat='batcat -p'
alias clip="xclip -selection clipboard"
alias csvt='. csvt'
alias ct='column -t'
alias dsp='docker system prune -f > /dev/null; docker images'
alias f="fdfind"
alias fa="fdfind -a"
alias faf="fdfind -a -t f"
alias fdd="fdfind -t d"
alias ff="fdfind -t f"
alias fp="fzf -m --preview 'batcat --style=numbers --color=always {} | head -500'"
alias ga='git add'
alias galias="alias | grep 'alias g' | grep -P '(^alias )\K.*' -o | sed 's/=/\t/g' | tr -d \' | grep -v 'galias' | grep -v 'grep' | sort | fzf"
alias gb='git branch'
alias gbdf='git branch -d -f $(git branch | fzf)'
alias gbl='git branch'
alias gblr='git branch -r'
alias gbn='git checkout -b'
alias gca='git add . && git commit --amend && git push --force'
alias gclp='gcloud projects list'
alias gcob='git checkout --track $(git branch -r | fzf)'
alias gdiff='git diff'
alias gfp='git fetch --prune'
alias gh='git log -1 --format=%h'
alias gl='git log'
alias glol='git log --oneline'
alias gp='git pull'
alias gpf='git push --force'
alias gpr='git pull --rebase'
alias gpush='git push'
alias gpushf='git push --force'
alias gpushsu='git push --set-upstream origin $(git branch --list | grep -Po "\* \K.*")'
alias gra='git rebase --abort'
alias grc='git rebase --continue'
alias grh='git reset --hard'
alias gst='git status'
alias gt='git tag'
alias gtd='git tag -d'
alias gtl='git tag -l | sort --version-sort'
alias gtr='gretag'
alias gwip='ga . && gcm "WIP $(date +"%Y-%m-%d %H:%M:%S")" && gpush'
alias ht='helm template .'
alias hta='helm template . | kubectl apply -f -'
alias i='istioctl'
alias ipc='ipcalc'
alias k='kubectl'
alias ka='kubectl -n argocd'
alias kap='kubectl apply -f'
alias kd='kubectl describe'
alias ke='KUBE_EDITOR="code --wait" kubectl edit'
alias kg='kubectl get'
alias kgn='kubectl get nodes'
alias ki='kubectl -n istio-system'
alias ko='kubectl -n istio-operator'
alias kpo='kubectl get pods'
alias ks='kubectl -n kube-system'
alias l1="ls -1 --color=auto"
alias la="ls -la"
alias lc="ls | column -c 1"
alias lh="ls -lh"
alias lha="ls -lha"
alias lower='tr "[:upper:]" "[:lower:]"'
alias mem='free -h'
alias mod='stat -c "%a"'
alias mp='multipass'
alias mpalias="alias | grep -E '(^alias).*(multipass).*' | sed 's/alias //' | column -t -s '=' | tr -d \' | sed '/^mpalias/ d'"
alias mph='multipass stop'
alias mpl='multipass list'
alias mps='multipass start'
alias mpsu='multipass suspend'
alias now='date +"%Y-%m-%d %H:%M:%S"'
alias os='openstack'
alias pwc='echo $(pwd) && echo -n $(pwd) | clip'
alias rmd='rm -rf'
alias sb='stackbuild'
alias sr='stackrun'
alias t='tree'
alias tdc='cd ~/tdc'
alias tf='terraform'
alias tfa='terraform apply -auto-approve'
alias tfap='terraform apply -auto-approve ${HOME}/terraform/output/terraform.plan'
alias tfar='terraform apply -auto-approve -refresh-only'
alias tfc="tfclear"
alias tfd='terraform destroy -auto-approve'
alias tfg='SVG_FILE=~/Pictures/$(basename ${PWD})_$(date +"%Y-%m-%d_%H_%M_%S").svg && terraform graph | dot -Tsvg > ${SVG_FILE?}; echo ${SVG_FILE?}'
alias tfip='tfi && terraform plan -out ${HOME}/terraform/output/terraform.plan'
alias tfipa='tfi && terraform plan -out ${HOME}/terraform/output/terraform.plan && terraform apply -auto-approve ${HOME}/terraform/output/terraform.plan'
alias tfo='terraform output'
alias tfoc='terraform output | column -t'
alias tfoj='terraform output -json | jq'
alias tfp='terraform plan -out ${HOME}/terraform/output/terraform.plan'
alias tfs='tfswitch'
alias tfscan="terrascan scan"
alias tfsl='terraform state list'
alias tfvars='ln -s ~/.terraform.tfvars terraform.tfvars'
alias tfw='terraform workspace'
alias tfwl='terraform workspace list'
alias trans='trans -t pt --brief --no-auto'
alias tx='tmux'
alias txn='tmux new -s "local"'
alias upper='tr "[:lower:]" "[:upper:]"'
alias vg='vagrant'
alias vgd='vagrant destroy -f'
alias vgh='vagrant halt'
alias vgr='vagrant reload'
alias vgs='vagrant status'
alias vgsu='vagrant suspend'
alias vgu='vagrant up'
alias wasp="kubectl wasp"
alias xa='xargs'
alias xa1='xargs -n 1'
alias xai='xargs -n 1 -I {}'
alias yq='yq -C'
alias ytop='ytop -c monokai'
