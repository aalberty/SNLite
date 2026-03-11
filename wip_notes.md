commands:
search (table, query, format{none, list, form})


rather than taking a 'commands in a repl' approach with commands being API calls, commands should interact with the UI primarily, and the API call should be a result of user interacting with the view in a way that *should* trigger api call (e.g. updating the query)

then your commands become:

pinned.add(<record>)
pinned.remove(<record>)
results.sort(field, [a/de]scending)
current.setValue(field, val) <-- where current is the currently displayed form
list.addColumn(field, position)
list.groupBy(field)
list.setColumnWidth(field, width)
etc.