# vim-clap

```vim
command! -bang -nargs=* -bar -range -complete=customlist,clap#helper#complete Clap call clap#(<bang>0, <f-args>)
```
