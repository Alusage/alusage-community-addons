On res.users form you can choose the default top menu .. Apps will be the menu with this default top menu as parent_id.

Managing top menus (Settings > Users & Companies > Top Menus)
-------------------------------------------------------------

* Click "New" to create a top menu. Its sub-menus are the applications shown to the users who
  have it as their top menu. The top menu flag is set automatically.
* Add sub-menus directly in the "Sub-menus" tab, or use "Add an Existing Menu" to add an existing
  menu (with its sub-menus) under any menu of the top menu. Two modes:

  * *Synchronized with the source menu*: the copy uses the same action (so the same views)
    and follows the name, sequence, action and access groups of the source menu.
  * *Duplicated (independent copy)*: the action and its views are duplicated, the access
    groups are copied and then can be changed without impacting the source menu.

* The mode is chosen when the menu is added and cannot be changed afterwards.
* "Synchronize with Sources" on a top menu or a menu refreshes the synchronized copies, including
  sub-menus added to the source since the copy was made. Duplicated copies are not affected.
* Access rights per model (ir.model.access) are not duplicated: they are shared by all menus
  opening the same model.
* Deleting a menu inside a top menu also deletes its sub-menus.
* Administrators see top menus as applications like any other menu.
