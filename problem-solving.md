2019-11-09

**Correctly Import libtcod**
- >`Unable to import 'tcod'pylint(import-error)`
- https://stackoverflow.com/questions/53074663/how-to-properly-import-libtcod-in-pycharm
- typed in command
  - `python -m pip install tcod`

**Change default tab-space size to 4 to match tutorial**
- https://stackoverflow.com/questions/42118651/how-to-set-python-language-specific-tab-spacing-in-visual-studio-code
- change json file
  - ```json
        "[python]": {
          "editor.insertSpaces": true,
          "editor.tabSize": 4
        }
    ```

2019-11-12

**FOV isn't working**
- fov is working now.  I had some crufty old mixed-up code that was blocking it.  blarg.  blarg blarg blarg.  👍👍👍👍👍👍

**subtask: fix deprecration warnings**

- [X] uuuuuuuuuuuuuuuuuugh
-

2019-11-13

**String interoplation or something**

```python
print({} + {}, "rooms", len(game_map.rooms))
```

2019-11-14

- [ ] Get that room assignment on the go
- [X] Fix those deprecation warnings
  - [X] uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuugh
  - [X] uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuugh
  - [X] uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuugh
  - [X] uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuugh
  - [X] uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuugh
  - [X] uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuugh
  - [X] uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuugh
  - [X] Well, you got somewhere, so there's that, which is nice
    `while not tcod.event == 'QUIT':`
    - can't find old, so whatever 🤷‍
- problem now is the x button doesn't work, when you try to close it.  'Esc' still works, but not the X button.  how vex.  I am vex.  vex vex vex 🐱‍👓