# Personal-Space
Local website to manage personal information

## Usage

STEP 1. Create file `config.json` in the root directory.

```json
{
  "logo": "My logo",
  "wiki": "{path-to-wiki-root}",
  "calendar": "{path-to-calendar-root}",
  "contacts": "{path-to-contacts-root}"
}
```

STEP 2. Install dependencies

Use the following command to install dependencies:

```shell
pip install -r requirements.txt
```

STEP 3. Start the server


```shell
python app.py
```

## Folders Structure

### Wiki Folder

Wiki folder contains all the markdown files.

### Calendar Folder

The calendar folder contains subfolders for every day. The subfolder name should be `YYYY-MMDD`. For example, `2026-0324` is March 24.  Each day contains meetings and tasks.

#### Meetings

The meeting file should have the following name: `HHMM - Title.md`. For example `0845 - Weekly status report.md `. The markdown file should include the following metadata header:

```yaml
title: Weekly status report
date: 2026-03-23
time: 2026-03-23 08:45:00-06:00
duration: 30
size: Large
organizer: John Doe
repeats: weekly
tags:
  - calendar
```

The contact subfolder may also contain images. The first image will be used as a “mugshot” when the contact is displayed on the page.

**Tags.** The `tags` field must have at least one tag: `calendar`. There are four tags that will be displayed on UI as icons. See the tags and icons below.

#### Tasks

The task file should have the following name: `TODO - Title.md`. For example `TODO - Finish testing.md `. The markdown file should include the following metadata header:

```yaml
title: Finish testing
created: 2026-03-13
priority: Today
due: 2026-05-10
next: Next task
project: Project Name
status: Active
tags:
  - todo
```

The contact subfolder may also contain images. The first image will be used as a “mugshot” when the contact is displayed on the page.



**Due Date.** The `due` field is optional. By default the task does not have due date.



**Priority.** The `priority` field may have one of the following values:

- “Today”: The tasks you need to focus on today.
- “Week”: The tasks you may finish during this week.
- “Month”: The task may require several weeks to complete, or you may wait for several weeks before you start them.
- “Year”: All other tasks that you may need to do eventually.



**Status.** The `status` field may have one of the following values:

- “Open”: The initial status assigned when you create a new task.
- “Active”: The task is in progress. You are actively working on this.
- “Urgent”: The task has the high priority.
- “Overdue”: The task is overdue. You must attend to it now.
- “Ready”: The work is ready, you need to verify the status before you call it completed.
- “Done”: This is the final status of the task. When you close the task, the application changes status to Done and rename the file to “DONE - Title”.



**Tags.** The `tags` field must have at least one tag: `todo`. There are four tags that will be displayed on UI as icons. See the tags and icons below.



#### Tags and Icons

- `important`: the items with this tag will be shown with ❗icon,
- `question`: the items with this tag will be shown with ❓icon,
- `person`: the items with this tag will be shown with 👨️ icon,
- `call`: the items with this tag will be shown with 📞 icon.



### Contacts Folder

The contacts folder contains subfolders for contacts. You can choose any naming system for subfolders and files. The application will pickup all markdown files in all subfolders. The contact markdown file should include the following metadata header:

```yaml
FirstName: John
LastName: Doe
face: "[[face-image.jpg]]"
title: Job Title
location: Miami Lakes, FL
timezone: UTC-5
team: Category
tags:
  - people
```

The contact subfolder may also contain images. The first image will be used as a “mugshot” when the contact is displayed on the page.

**Tags.** The `tags` field must have at least one tag: `people`.