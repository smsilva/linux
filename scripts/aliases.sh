alias bat='batcat'
alias cat='bat -p'
alias clip="xclip -selection clipboard"
alias ct='column -t'
alias csvt='. csvt'

alias fd="fdfind"
alias ff="fd -t f"
alias fdd="fd -t d"
alias fp="fzf -m --preview 'batcat --style=numbers --color=always {} | head -500'"
alias fpa="fdfind --type f --hidden --follow --exclude .git | fzf -m --preview 'bat --style=numbers --color=always {} | head -500'"

alias ht='helm template .'
alias hta='helm template . | kubectl apply -f -'

alias i='istioctl'
alias k='kubectl'
alias ka='kubectl -n argocd'
alias ki='kubectl -n istio-system'
alias ko='kubectl -n istio-operator'
alias ks='kubectl -n kube-system'
alias kap='kubectl apply -f'
alias kgn='kubectl get nodes'
alias kpo='kubectl get pods'

alias l1="ls -1 --color=auto"
alias la="ls -la"
alias lc="ls | column -c 1"
alias lh="ls -lh"

alias lower='tr "[:upper:]" "[:lower:]"'

alias mem='free -h'

alias mpalias="alias | grep -E '(^alias).*(multipass).*' | sed 's/alias //' | column -t -s '=' | tr -d \' | sed '/^mpalias/ d'"
alias mp='multipass'
alias mph='multipass stop'
alias mpl='multipass list'
alias mps='multipass start'
alias mpsu='multipass suspend'

alias pwc='echo $(pwd) && echo -n $(pwd) | clip'

alias tx='tmux'
alias txn='tmux new -s "local"'

alias galias="alias | grep 'alias g' | grep -P '(^alias )\K.*' -o | sed 's/=/\t/g' | tr -d \' | grep -v 'galias' | grep -v 'grep' | sort | fzf"
# alias | grep 'alias g' | awk -F "'" '{ print $1 "|" $2 }' | sed 's/^alias //; s/=|/#/; /^galias/d' | column -t -s "#" | fzf

alias gb='git branch'
alias gbn='git checkout -b'
alias gbd='git branch -d $(git branch | fzf)'
alias gbdf='git branch -d -f $(git branch | fzf)'
alias gbl='git branch'
alias gblr='git branch -r'
alias gcob='git checkout --track $(git branch -r | fzf)'
alias gdiff='git diff'
alias gfp='git fetch --prune'
alias gp='git pull'
alias gpr='git pull --rebase'
alias gst='git status'
alias gpf='git push --force'
alias gl='git log'
alias glol='git log --oneline'
alias ga='git add'
alias gcm='git commit -m'
alias grh='git reset --hard'
alias gr='git rebase'
alias gpush='git push'
alias gpushf='git push --force'
alias gpushsu='git push --set-upstream origin $(git branch --list | grep -Po "\* \K.*")'
alias vg='vagrant'
alias vgs='vagrant status' 
alias vgu='vagrant up'
alias vgd='vagrant destroy -f'
alias vgh='vagrant halt'
alias vgsu='vagrant suspend'
alias vgr='vagrant reload'

alias now='date +"%Y-%m-%d %H:%M:%S"'
alias trans='trans -t pt --brief --no-auto'

alias ytop='ytop -c monokai'
alias yq='yq -C'
