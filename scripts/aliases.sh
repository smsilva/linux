alias bat='batcat'
alias cat='bat -p'
alias clip="xclip -selection clipboard"

alias fd="fdfind"
alias ff="fd -t f"
alias fdd="fd -t d"
alias fp="fzf -m --preview 'bat --style=numbers --color=always {} | head -500'"
alias fpa="fdfind --type f --hidden --follow --exclude .git | fzf -m --preview 'bat --style=numbers --color=always {} | head -500'"

alias k='kubectl'

alias la="ls -la"
alias lc="ls | column -c 1"
alias lh="ls -lh"

alias mem='free -h'
alias pwc='echo $(pwd) && echo -n $(pwd) | clip'

alias tx='tmux'
alias txn='tmux new -s "local"'

alias galias="alias | grep 'alias g' | grep -P '(^alias )\K.*' -o | sed 's/=/\t/g' | tr -d \' | grep -v 'galias' | grep -v 'grep' | sort"
alias gcob='git checkout --track $(git branch -r | fzf)'
alias gbd='git branch -d $(git branch | fzf)'
alias gbdf='git branch -d -f $(git branch | fzf)'
alias gbl='git branch'
alias gblr='git branch -r'
alias gdiff='git diff'
alias gp='git pull'
alias gpr='git pull --rebase'
alias gst='git status'
alias gpf='git push --force'
alias gl='git log'
alias glol='git log --oneline'
alias ga='git add'
alias gcm='git commit -m'
alias grh='git reset --hard'
alias gpush='git push'
alias gpushf='git push --force'

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
