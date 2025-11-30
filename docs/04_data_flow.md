# Data Flow & Interaction Patterns

This guide traces how data flows through Eldritch Tactics, from user input to screen display.

## Complete System Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER RUNS APPLICATION                        │
│                    uv run python main.py                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         main.py                                 │
│  1. pygame.init()          ← Initialize all Pygame systems      │
│  2. create screen Surface  ← 1920x1080 fullscreen window        │
│  3. create Clock           ← For FPS control                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              title_screen = TitleScreen(screen)                 │
│                                                                 │
│  TitleScreen.__init__():                                        │
│    ├─ Calculate screen center (960, 540)                        │
│    ├─ Create TextLabels (title, subtitle, flavor)              │
│    ├─ Create 4 MenuButtons                                      │
│    │    ├─ New Game    → on_new_game()                          │
│    │    ├─ Continue    → on_continue()     (disabled)           │
│    │    ├─ Settings    → on_settings()                          │
│    │    └─ Exit        → on_exit()                              │
│    └─ Store buttons in self.buttons list                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│               next_screen = title_screen.run(clock)             │
│                                                                 │
│  ╔══════════════════════════════════════════════════════════╗  │
│  ║            GAME LOOP (60 FPS)                            ║  │
│  ║                                                          ║  │
│  ║  while self.running:                                     ║  │
│  ║      ┌────────────────────────────────────────────┐     ║  │
│  ║      │ 1. handle_events()                         │     ║  │
│  ║      │    for event in pygame.event.get():        │     ║  │
│  ║      │        - Check QUIT, KEYDOWN                │     ║  │
│  ║      │        - Forward to all buttons             │     ║  │
│  ║      └────────────────────────────────────────────┘     ║  │
│  ║                         ↓                                ║  │
│  ║      ┌────────────────────────────────────────────┐     ║  │
│  ║      │ 2. update()                                │     ║  │
│  ║      │    mouse_pos = get_pos()                   │     ║  │
│  ║      │    for button in self.buttons:             │     ║  │
│  ║      │        button.update(mouse_pos)            │     ║  │
│  ║      └────────────────────────────────────────────┘     ║  │
│  ║                         ↓                                ║  │
│  ║      ┌────────────────────────────────────────────┐     ║  │
│  ║      │ 3. draw()                                  │     ║  │
│  ║      │    screen.fill(COLOR_BG)                   │     ║  │
│  ║      │    title.draw(screen)                      │     ║  │
│  ║      │    for button in self.buttons:             │     ║  │
│  ║      │        button.draw(screen)                 │     ║  │
│  ║      └────────────────────────────────────────────┘     ║  │
│  ║                         ↓                                ║  │
│  ║      ┌────────────────────────────────────────────┐     ║  │
│  ║      │ 4. pygame.display.flip()                   │     ║  │
│  ║      │    Show hidden buffer on screen            │     ║  │
│  ║      └────────────────────────────────────────────┘     ║  │
│  ║                         ↓                                ║  │
│  ║      ┌────────────────────────────────────────────┐     ║  │
│  ║      │ 5. clock.tick(60)                          │     ║  │
│  ║      │    Wait to maintain 60 FPS                 │     ║  │
│  ║      └────────────────────────────────────────────┘     ║  │
│  ║                         ↓                                ║  │
│  ║            (Loop repeats)                                ║  │
│  ║                                                          ║  │
│  ║  User clicks "New Game":                                 ║  │
│  ║    Button detects click → calls on_new_game() →         ║  │
│  ║      Sets self.running = False                           ║  │
│  ║        Loop exits                                        ║  │
│  ╚══════════════════════════════════════════════════════════╝  │
│                              │                                  │
│  return self.next_screen  # "new_game"                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Back in main.py                            │
│                                                                 │
│  if next_screen == "new_game":                                  │
│      print("Starting new game...")                              │
│      # TODO: battle = BattleScreen(screen)                      │
│      # TODO: next_screen = battle.run(clock)                    │
│                                                                 │
│  pygame.quit()                                                  │
│  sys.exit(0)                                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Mouse Click Flow - Detailed

Let's trace **exactly** what happens when you click the "New Game" button:

### Frame 1-59: Hovering

```
Every frame:
1. title_screen.update():
     mouse_pos = (850, 500)  # User hovering over button
     new_game_button.update(mouse_pos)
        └─ is_hovered = rect.collidepoint((850, 500))
        └─ is_hovered = True

2. title_screen.draw():
     new_game_button.draw(screen)
        └─ Uses color_hover (lighter blue)
        └─ Border width = 3 (thicker)
        └─ Text color = golden

User sees: Button is highlighted, showing it's interactive
```

### Frame 60: Mouse Press Down

```
1. title_screen.handle_events():
     event = MOUSEBUTTONDOWN at (850, 500), button=1

     new_game_button.handle_event(event):
        ├─ event.type == MOUSEBUTTONDOWN? YES
        ├─ event.button == 1? YES (left click)
        ├─ self.is_hovered? YES (mouse is on button)
        ├─ self.is_pressed = True
        └─ return False (not complete yet)

2. title_screen.update():
     new_game_button.update(mouse_pos)
        └─ is_hovered = True (still on button)

3. title_screen.draw():
     new_game_button.draw(screen)
        └─ is_pressed = True
        └─ Uses color_active (brightest blue)

User sees: Button gets even brighter (visual feedback for press)
```

### Frame 61: Mouse Released

```
1. title_screen.handle_events():
     event = MOUSEBUTTONUP at (850, 500), button=1

     new_game_button.handle_event(event):
        ├─ event.type == MOUSEBUTTONUP? YES
        ├─ event.button == 1? YES
        ├─ self.is_hovered? YES
        ├─ self.is_pressed? YES
        ├─ COMPLETE CLICK DETECTED!
        ├─ self.is_pressed = False
        ├─ self.on_click()  ← EXECUTE CALLBACK
        │    └─ on_new_game() runs:
        │         ├─ print("New Game selected")
        │         ├─ self.next_screen = "new_game"
        │         └─ self.running = False  ← EXIT LOOP!
        └─ return True

2. Loop condition checked:
     while self.running:  ← self.running is now False!
        └─ Loop exits

3. return self.next_screen
     └─ Returns "new_game" to main.py

Control returns to main.py with choice = "new_game"
```

---

## Event Propagation

How events flow from OS to UI components:

```
┌─────────────────────────────────────────────────────────────┐
│  1. USER CLICKS MOUSE                                       │
└─────────────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  2. OPERATING SYSTEM                                        │
│     Generates mouse event                                   │
│     Contains: position, button number, timestamp            │
└─────────────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  3. PYGAME-CE                                               │
│     SDL2 layer captures OS event                            │
│     Converts to pygame.event.Event                          │
│     Adds to event queue                                     │
└─────────────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  4. pygame.event.get()                                      │
│     Retrieves all queued events                             │
│     Returns list of Event objects                           │
│     Clears the queue                                        │
└─────────────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  5. title_screen.handle_events()                            │
│     for event in pygame.event.get():                        │
│         # Check window close                                │
│         if event.type == pygame.QUIT: ...                   │
│                                                             │
│         # Check keyboard                                    │
│         if event.type == pygame.KEYDOWN: ...                │
│                                                             │
│         # Forward to ALL buttons                            │
│         for button in self.buttons:                         │
│             button.handle_event(event)                      │
└─────────────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  6. button.handle_event(event)                              │
│     Each button checks:                                     │
│     "Was this click on ME?"                                 │
│                                                             │
│     if event.type == MOUSEBUTTONDOWN:                       │
│         if self.is_hovered:  ← Only this button responds    │
│             self.is_pressed = True                          │
└─────────────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  7. CALLBACK EXECUTION                                      │
│     if self.on_click:                                       │
│         self.on_click()  ← Runs user's function            │
│                                                             │
│     def on_new_game(self):                                  │
│         self.next_screen = "new_game"                       │
│         self.running = False                                │
└─────────────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  8. GAME LOOP EXITS                                         │
│     while self.running:  ← Now False                        │
│         # Loop ends                                         │
│                                                             │
│     return self.next_screen  ← "new_game"                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Rendering Pipeline

How the screen gets drawn each frame:

```
┌───────────────────────────────────────────────────────────────┐
│  FRAME START (1/60 second)                                    │
└───────────────────────────────────────────────────────────────┘
                     ↓
┌───────────────────────────────────────────────────────────────┐
│  1. CLEAR SCREEN                                              │
│     screen.fill(COLOR_BG)                                     │
│                                                               │
│     [████████████████████████████] ← Entire screen dark blue  │
└───────────────────────────────────────────────────────────────┘
                     ↓
┌───────────────────────────────────────────────────────────────┐
│  2. DRAW TITLE                                                │
│     title.draw(screen)                                        │
│                                                               │
│     [███ ELDRITCH TACTICS ███] ← Title text added             │
│     [████████████████████████████]                            │
└───────────────────────────────────────────────────────────────┘
                     ↓
┌───────────────────────────────────────────────────────────────┐
│  3. DRAW SUBTITLE                                             │
│     subtitle.draw(screen)                                     │
│                                                               │
│     [███ ELDRITCH TACTICS ███]                                │
│     [█ Lovecraftian... ██████]                                │
│     [████████████████████████████]                            │
└───────────────────────────────────────────────────────────────┘
                     ↓
┌───────────────────────────────────────────────────────────────┐
│  4. DRAW BUTTONS (in list order)                              │
│     for button in self.buttons:                               │
│         button.draw(screen)                                   │
│                                                               │
│  Each button.draw():                                          │
│    ├─ Draw filled rectangle (button background)              │
│    ├─ Draw border (outline)                                  │
│    └─ Draw text (centered)                                   │
│                                                               │
│     [███ ELDRITCH TACTICS ███]                                │
│     [█ Lovecraftian... ██████]                                │
│     [████████████████████████████]                            │
│     [████ [New Game] █████████████]                           │
│     [████ [Continue] ██████████████]                          │
│     [████ [Settings] ██████████████]                          │
│     [████ [Exit] ███████████████████]                         │
└───────────────────────────────────────────────────────────────┘
                     ↓
┌───────────────────────────────────────────────────────────────┐
│  5. DRAW FLAVOR TEXT                                          │
│     flavor_text.draw(screen)                                  │
│                                                               │
│     [███ ELDRITCH TACTICS ███]                                │
│     [█ Lovecraftian... ██████]                                │
│     [████████████████████████████]                            │
│     [████ [New Game] █████████████]                           │
│     [████ [Continue] ██████████████]                          │
│     [████ [Settings] ██████████████]                          │
│     [████ [Exit] ███████████████████]                         │
│     [████████████████████████████]                            │
│     [██ The stars are right... ██]                            │
│     [██ v0.1.0 ████████████████████]                          │
└───────────────────────────────────────────────────────────────┘
                     ↓
┌───────────────────────────────────────────────────────────────┐
│  6. DOUBLE BUFFER SWAP                                        │
│     pygame.display.flip()                                     │
│                                                               │
│  Hidden Buffer ──swap──> Visible Screen                       │
│                                                               │
│  User sees completed frame                                    │
└───────────────────────────────────────────────────────────────┘
                     ↓
┌───────────────────────────────────────────────────────────────┐
│  7. FRAMERATE CONTROL                                         │
│     clock.tick(60)                                            │
│                                                               │
│  Elapsed time: 10ms                                           │
│  Target time: 16.67ms (60 FPS)                                │
│  Wait: 6.67ms                                                 │
└───────────────────────────────────────────────────────────────┘
                     ↓
             NEXT FRAME STARTS
```

---

## State Transitions

Button states change based on user interaction:

```
┌─────────────┐
│   NORMAL    │  is_hovered=False, is_pressed=False
│  (idle)     │  Color: COLOR_MENU_BUTTON (dark)
└─────────────┘
       │
       │ Mouse moves over button
       │ update() detects: rect.collidepoint(mouse_pos)
       ↓
┌─────────────┐
│   HOVERED   │  is_hovered=True, is_pressed=False
│ (mouseover) │  Color: COLOR_MENU_BUTTON_HOVER (lighter)
└─────────────┘  Border: 3px (thicker)
       │
       │ User presses mouse down
       │ handle_event(MOUSEBUTTONDOWN)
       ↓
┌─────────────┐
│   PRESSED   │  is_hovered=True, is_pressed=True
│ (clicking)  │  Color: COLOR_MENU_BUTTON_ACTIVE (brightest)
└─────────────┘
       │
       ├─ Mouse released on button
       │  handle_event(MOUSEBUTTONUP)
       │  → EXECUTE CALLBACK
       │  → exit to main.py
       │
       └─ Mouse dragged away
          (is_hovered becomes False)
          → No callback, return to NORMAL
```

---

## Memory Layout

Where data lives in RAM:

```
┌──────────────────────────────────────────────────────────────┐
│  PYTHON HEAP                                                 │
│                                                              │
│  main.py variables:                                          │
│    screen: Surface → [1920x1080 pixel buffer ~8MB]          │
│    clock: Clock → [timing data ~100 bytes]                  │
│    title_screen: TitleScreen → ┐                            │
│                                 │                            │
│  ┌──────────────────────────────┘                            │
│  │                                                           │
│  │  TitleScreen instance (~10KB):                            │
│  │    self.screen: reference to main's screen               │
│  │    self.running: bool (1 byte)                            │
│  │    self.next_screen: str or None (~20 bytes)             │
│  │    self.buttons: list → [                                │
│  │       MenuButton instance (~500 bytes)                    │
│  │       MenuButton instance (~500 bytes)                    │
│  │       MenuButton instance (~500 bytes)                    │
│  │       MenuButton instance (~500 bytes)                    │
│  │    ]                                                      │
│  │    self.title: TextLabel instance (~200 bytes)           │
│  │    self.subtitle: TextLabel instance (~200 bytes)        │
│  │    self.flavor_text: TextLabel instance (~200 bytes)     │
│  │                                                           │
│  │  Each MenuButton instance:                                │
│  │    self.rect: Rect (16 bytes)                             │
│  │    self.text: str (~20 bytes)                             │
│  │    self.on_click: function reference (8 bytes)           │
│  │    self.is_hovered: bool (1 byte)                         │
│  │    self.is_pressed: bool (1 byte)                         │
│  │    self.colors: tuples (~100 bytes)                       │
│  │    (+ inherited Button attributes)                        │
│  │                                                           │
│  └───────────────────────────────────────────────────────────│
│                                                              │
│  Total title screen memory: ~12KB (negligible)              │
│  Total screen buffer: ~8MB (most memory)                    │
└──────────────────────────────────────────────────────────────┘
```

---

## Timing Breakdown

What happens in one 60 FPS frame (16.67ms budget):

```
Frame Timeline (Target: 16.67ms @ 60 FPS)
═══════════════════════════════════════════════════════════

0.00ms  ┬─ handle_events()
        │  ├─ pygame.event.get()           (0.05ms)
        │  ├─ Check QUIT, KEYDOWN           (0.01ms)
        │  └─ Forward to 4 buttons          (0.04ms)
0.10ms  ┤

0.10ms  ├─ update()
        │  ├─ pygame.mouse.get_pos()        (0.01ms)
        │  └─ Update 4 buttons              (0.04ms)
0.15ms  ┤

0.15ms  ├─ draw()
        │  ├─ screen.fill()                 (0.5ms)  ← Most time
        │  ├─ Draw 3 labels                 (0.3ms)
        │  │  └─ font.render() × 3
        │  └─ Draw 4 buttons                (0.4ms)
        │     └─ font.render() × 4
1.35ms  ┤

1.35ms  ├─ pygame.display.flip()
        │  └─ GPU buffer swap               (0.1ms)
1.45ms  ┤

1.45ms  ├─ clock.tick(60)
        │  └─ Sleep to maintain 60 FPS      (15.22ms) ← Wait time
16.67ms ┴

Total CPU work: ~1.45ms
Waiting: ~15.22ms
```

**Why so much waiting?**
- We finish rendering in ~1.5ms
- Target is 16.67ms per frame
- `clock.tick(60)` waits the remaining ~15ms
- This prevents wasting CPU and maintains consistent FPS

---

## Future: Multiple Screen Navigation

When battle screen is added:

```
main.py:
    ├─ Show title screen
    │    ├─ User clicks "New Game"
    │    └─ Returns "new_game"
    │
    ├─ Show battle screen
    │    ├─ User wins battle
    │    └─ Returns "campaign"
    │
    ├─ Show campaign screen
    │    ├─ User selects mission
    │    └─ Returns "battle"
    │
    └─ Loop continues...

Structure:
    while game_running:
        if next_screen == "title":
            title = TitleScreen(screen)
            next_screen = title.run(clock)

        elif next_screen == "battle":
            battle = BattleScreen(screen, mission_data)
            next_screen = battle.run(clock)

        elif next_screen == "campaign":
            campaign = CampaignScreen(screen, save_data)
            next_screen = campaign.run(clock)

        elif next_screen == "exit":
            game_running = False
```

---

## Debugging Data Flow

### Adding Debug Prints

Track event flow:

```python
def handle_events(self):
    for event in pygame.event.get():
        print(f"Event: {pygame.event.event_name(event.type)}")

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(f"  Mouse down at {event.pos}, button {event.button}")

        for button in self.buttons:
            clicked = button.handle_event(event)
            if clicked:
                print(f"  Button '{button.text}' was clicked!")
```

### Visualizing State

Draw debug overlays:

```python
def draw(self):
    # Normal drawing
    self.screen.fill(config.COLOR_BG)
    # ... draw UI ...

    # Debug overlay
    if DEBUG_MODE:
        # Show button hitboxes
        for button in self.buttons:
            pygame.draw.rect(screen, (255, 0, 0), button.rect, 2)

        # Show mouse position
        mouse_pos = pygame.mouse.get_pos()
        font = pygame.font.Font(None, 24)
        text = font.render(f"Mouse: {mouse_pos}", True, (255, 255, 0))
        screen.blit(text, (10, 10))
```

---

## Battle Screen - Movement Activation Flow

The battle screen uses a **movement mode state machine** to control when green tile highlights appear.

### Movement Mode State Machine

```
┌─────────────────────────────────────────────────────────────┐
│                    MOVEMENT MODE STATES                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  State: INACTIVE (default)                                 │
│  ├─ movement_mode_active = False                           │
│  ├─ show_movement_range = False                            │
│  └─ No green tiles visible                                 │
│                        │                                    │
│                        │ User clicks Move button (slot 0)  │
│                        │ or presses hotkey '1'             │
│                        ▼                                    │
│  State: ACTIVE                                              │
│  ├─ movement_mode_active = True                            │
│  ├─ show_movement_range = True                             │
│  ├─ reachable_tiles calculated (flood-fill)                │
│  └─ Green highlights drawn on grid                         │
│                        │                                    │
│         ┌──────────────┼──────────────┬─────────────┐      │
│         │              │              │             │      │
│    Unit moves   Turn ends   Unit selected   Attack │      │
│         │              │              │             │      │
│         └──────────────┴──────────────┴─────────────┘      │
│                        │                                    │
│                        ▼                                    │
│  State: INACTIVE (reset)                                    │
│  └─ deactivate_movement_mode() called                      │
└─────────────────────────────────────────────────────────────┘
```

### User Clicks Move Button - Complete Flow

```
Frame 1: User clicks Move button (slot 0)
┌──────────────────────────────────────────────────────────┐
│ 1. ActionButton.handle_event(MOUSEBUTTONDOWN)           │
│    ├─ is_hovered? YES                                    │
│    ├─ is_pressed = True                                  │
│    └─ return False (wait for BUTTONUP)                   │
└──────────────────────────────────────────────────────────┘

Frame 2: User releases mouse
┌──────────────────────────────────────────────────────────┐
│ 2. ActionButton.handle_event(MOUSEBUTTONUP)             │
│    ├─ is_hovered? YES                                    │
│    ├─ is_pressed? YES                                    │
│    ├─ CLICK DETECTED!                                    │
│    ├─ self.on_click()  [lambda: action_bar._on_action_click(0)]
│    └─ return True                                        │
│                                                          │
│ 3. ActionBar._on_action_click(slot_index=0)             │
│    ├─ print("Action slot 0 clicked")                    │
│    └─ self.on_action_click_callback(0)                  │
│          [BattleScreen._on_action_button_click]         │
│                                                          │
│ 4. BattleScreen._on_action_button_click(slot_index=0)   │
│    ├─ if slot_index == 0:  [Move action]                │
│    └─ self.activate_movement_mode()                     │
│                                                          │
│ 5. BattleScreen.activate_movement_mode()                │
│    ├─ Check: current_turn_unit is player? YES           │
│    ├─ Check: unit can move? YES                         │
│    ├─ Calculate reachable tiles (flood-fill)            │
│    │    └─ get_reachable_tiles(grid, pos, range)        │
│    │         └─ Returns set of (x, y) coordinates       │
│    ├─ self.reachable_tiles = {(0,3), (1,2), ...}        │
│    ├─ self.movement_mode_active = True                  │
│    ├─ self.show_movement_range = True                   │
│    └─ print("Movement mode activated - 48 tiles...")    │
└──────────────────────────────────────────────────────────┘

Frame 3+: Green tiles now visible
┌──────────────────────────────────────────────────────────┐
│ 6. BattleScreen.draw()                                   │
│    └─ self._draw_grid()                                  │
│         ├─ for each tile in grid:                        │
│         │    ├─ is_reachable = (x,y) in self.reachable_tiles
│         │    ├─ if is_reachable:                         │
│         │    │    ├─ color = (40, 60, 40)  [green tint]  │
│         │    │    └─ pygame.draw.rect(..., 2)  [border]  │
│         │    └─ else:                                    │
│         │         └─ color = normal                      │
│         └─ User sees green highlighted tiles!            │
└──────────────────────────────────────────────────────────┘
```

### User Clicks Green Tile - Movement Execution

```
User clicks on green tile (3, 5)
┌──────────────────────────────────────────────────────────┐
│ 1. BattleScreen._handle_left_click(mouse_pos)            │
│    ├─ grid_x, grid_y = _pixel_to_grid(mouse_pos)        │
│    │    └─ Returns (3, 5)                                │
│    ├─ tile = grid.get_tile(3, 5)                        │
│    ├─ tile.is_occupied()? NO                            │
│    └─ self._try_move_to_tile(3, 5)                      │
│                                                          │
│ 2. BattleScreen._try_move_to_tile(target_x=3, target_y=5)
│    ├─ Check: (3,5) in reachable_tiles? YES              │
│    ├─ current_pos = current_turn_unit.position  # (0,2) │
│    ├─ path = find_path(grid, 0, 2, 3, 5, max_dist=4)   │
│    │    └─ A* algorithm                                 │
│    │    └─ Returns [(0,2), (1,3), (2,4), (3,5)]        │
│    ├─ grid.move_unit(0, 2, 3, 5)                        │
│    │    ├─ from_tile.occupied_by = None                 │
│    │    ├─ to_tile.occupied_by = unit                   │
│    │    └─ unit.position = (3, 5)                       │
│    ├─ current_turn_unit.has_moved = True                │
│    ├─ print("Unit moved from (0,2) to (3,5)")           │
│    ├─ self._update_movement_range()  [recalculate]      │
│    └─ self.deactivate_movement_mode()                   │
│                                                          │
│ 3. BattleScreen.deactivate_movement_mode()              │
│    ├─ self.movement_mode_active = False                 │
│    ├─ self.show_movement_range = False                  │
│    └─ Green highlights disappear next frame             │
└──────────────────────────────────────────────────────────┘
```

### Key Differences from Title Screen

**Title Screen:**
- Click button → Immediate action (change screen)
- No state machine
- One-way flow

**Battle Screen Movement:**
- Click button → Enter mode (show options)
- State machine controls visibility
- Two-step interaction (activate → execute)
- Prevents accidental moves

**Benefits:**
- Explicit user intent required
- Visual feedback before commitment
- Matches tactical game conventions (X-COM, Fire Emblem)
- Extensible pattern for Attack, Abilities, etc.

---

## Summary

**Key Data Paths:**

1. **Input Flow:** OS → Pygame → Screen → Buttons → Callbacks
2. **Update Flow:** Mouse position → All buttons check hover
3. **Render Flow:** Background → UI elements → Flip buffer
4. **Navigation Flow:** Screen returns choice → main.py decides next screen

**Critical Concepts:**

- **Event queue** - Must be cleared every frame
- **Double buffering** - Draw to hidden, flip to visible
- **Callback pattern** - Components tell main code what happened
- **State management** - Screens control their own loop, return results

**Performance:**

- Rendering: ~1.5ms per frame
- Waiting: ~15ms (to maintain 60 FPS)
- Memory: ~8MB screen buffer + ~12KB UI data

---

## Next Steps

- [Pygame Fundamentals](01_pygame_fundamentals.md) - Core concepts
- [Architecture Overview](02_architecture_overview.md) - High-level structure
- [UI Components](03_ui_components.md) - Button internals

---

You now understand the complete flow of data through Eldritch Tactics! This knowledge will help you debug issues, optimize performance, and extend the system with new features.
