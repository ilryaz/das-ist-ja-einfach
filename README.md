<h1 align="center">
Das ist ja einfach!
</h1>
<h3 align="center">
  A productivity app that tracks your time in the most nonchalant way.
</h3>


## Features
- Full control of your subjects
- Weekly hourly goal for each one of them
- Study time track
- Quick-add study sessions using customizable time buttons
- Weekly progress monitoring
- Calendar-based study tracking
- Modern desktop interface built with Qt Widgets
- Multiple themes (including Catppuccin)
- Automatic data saving
- JSON-based persistence
- Automatic generation of missing data files from default templates
- Plugin-based architecture
- Modular design
- Separation of UI and data models
- Theme system based on templates and color palettes

## Installation

```bash
pip install PySide6
python main.py
```

## Screenshots

![1](screenshots/1.tiff)

## To-do
#### Add:
- [x] all data in json file
- [x] dark theme switcher
- [ ] commentaries for every day (general) and for every subject, then print them at the end of the week as a total (it should be a button that open a certain window in wihch one can add notes for the day's subjects and the week subjects, days should be switched via arrows)
- [x] add-time buttons can be deleted or added with a custom time
- [ ] theme autoloading

#### Fix:
- [x] when changing subject's name in edit mode it changes current subject in data, not create different one
- [x] fix week_config format and its usage everywhere
- [x] how themes look
- [ ] day buttons toggled no color indication
- [ ] fix buttons borders
