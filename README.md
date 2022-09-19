# dotfiles
my dotfiles :)

# `zsh-syntax-highlighting `

Install package with AUR `yay -S zsh-syntax-highlighting` and then copy the following line to the `.zshrc`
```
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
```

# ` zsh-autosuggestions ` 
Install `yay -S zsh-autosuggestions` and copy this line on  `.zshrc`
```
source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
```

# `Customize powerlevel10k`

Open `.p10k.zsh` and changes `DIR_FOREGROUND`
```
  typeset -g POWERLEVEL9K_DIR_FOREGROUND=232
```

and `DIR_ANCHOR_FOREGROUND` 

```
 typeset -g POWERLEVEL9K_DIR_ANCHOR_FOREGROUND=232
```
