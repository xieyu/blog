# Make Your First 2D Game With Godot

<!-- toc -->

## Part 1
### KinematicBody2D

控制角色运动和碰撞检测， 和RigionBody2D有什么区别？

1. CollisionShape2D: 碰撞检测, Geometric Shape: New RectTangeShape2D
2. Modulation: 调制，在inspector中可以改变collisionShape的颜色, 在debug模式比较有用.
3. Sprite, render顺序，从上到下，下面的覆盖上面的.
4. snaping feature: 用于精确放置图片到0点, snap to grid, 快捷键G Snap to pixel
5. collision shape比sprite稍微小一点.
6. Dector Monitorble是干啥的, 为啥要把Dector的physical Layer去掉？这样就不会发生碰撞检测了吗？只会做dector?
7. stampdector检测的时候，比较global_y 来判断player是否不是在头顶
8. player身上的enemyDector，jump更高一些, onAreaEnter和onBodyEnter有啥区别啊

```
src/Actors/Player.tscn
```

```
func _physic_process(delta: float) -> void:
  velocity.y = gravity * delta;
  velocity.y = max(velocity.y, speed.y)
  velocity = move_and_slide(velocity)

```

is_on_wall
is_on_floor

Actor.gd, player和enemy共享公用的代码


### TileMap

tileset.tres 这个制作细节需要去学习下

Cell collision, 给每个cell添加collsion，这个画完tilemap之后，自动就有了collision.
snapOptions: Step

CellSize

可以直接将Player drag到tilemap里面

physics layers
masks: 需要检测碰撞的layer

Input Mapping

get_action_strength


### Camera2D控制
Camera Limit: Top, left, Right, Bottom, Smoothed
Drag Margin, H,V enable


### LevelTemplate

rules: pixels, shiyong rules来衡量位置，然后修改camera的limit

### Background

TextureRectangle, Layout, FullRect

CanvasLayer-> Background, Layer -100, 
使用canvaslayer作为背景，这样背景图就这一直在了

## Part2: Coins, Portals and levels

### Coins

#### AnimationPlayer

##### 制作Coin的bouncing动画
length: 1.8s Add TracK
automatic key insert, 
uncheck rot 

AnimationTrackKeyEdit: Easing, 插值, 修改曲线
shirtf + D： player animation

AutoPlay on Load

coin.position


##### 制作Coin的Fadeout动画

修改CanvasItem/Visibility/Modulate的颜色, colorRange, 修改alpha值

在boucing动画中需要: Reset Modulate color

#### CallMethodTrack

在动画结束的时候，调用node的某个方法，比如fadeout动画结束了，call node的queueFree方法

### Portals: 下一个关卡的入口

CapsuleShape2D

TransitionLayer: CanvasLayer, ColorRectangle

canvas layer的行为和普通node不一样？render的时候.

#### fade in animation

animation player, canvaslayer ,visible 选择这个对性能影响比较大


## GUI: Menus/Pause/Score

代码目录结构

* Actors: 放player, enemies
* Levels: 各种关卡
* Objects: coins, portal 之类的小道具
* UserInterface: Menu/Title
* Screens: dialog

add node dialog中，green icon是gui node

control node: anchor/margin/rect/hint/focus etc.
ProjectSettings/MainScene/


### Background
Background: TextureRectangle, resizable texture for intereface.

背景和gui  Layout: FullRect, backgroud fits the parent

Label: basic text box, layout: centerTop


### VBoxContainer
Container: 将两个button放到container中, VBoxContainer

Button: Play,quit

Text, Ctl+D 复制一个button
同事选中buttons,然后在inspector中修改： Size Flags: Horizontal/Vectical Expand

两个button填充满VboxContainer

save branch as sencne, 将tree中部分node 保存成scene.

### Font

Theme: apply一个theme到node时候，所有的child都是用那个theme

在theme中修改font

DynamicFont, otf 文件拖到font data, 修改size

customerFonts, 

get_configuration_warning

ChangeSecneButton: reuseable button


MainScreen/EndScreen/PauseScreen


#### PlayerData

PlayerData相当于gameState, AutoLoad 单例模式

rest
set_score 之后发送一个singal score_updated

AutoLoad在ready中可以用


#### Pause

score:%s

retrybutton: get_tree().reload_current_scene() 重新加载当前scene

game_tree().paused = false, 使用这个来pause, pause时候所有东西都pause了

Inspector: Node/PauseMode: process 这样这个node就不会被pause了

get_tree().set_input_as_handled(); stop event的传播

player die的时候，就显示pause
