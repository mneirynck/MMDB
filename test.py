dataset = []
default_bg = {'red': 1, 'green': 1, 'blue': 1}
# all_data['sheets'] is a list of sheet resources (per the API spec.)
for sheet in all_data['sheets']:
    # The sheet resource is a dict with keys determined by what we requested in fields
    # (i.e. properties (->sheetId, ->title), data)
    print('Sheet name is {title} with grid id {sheetId}'.format_map(sheet["properties"]))
    # each range in data will only contain startRow and/or startColumn if they are not 0
    # (i.e. if you grab A1:___, you won't have startRow or startColumn)
    for range in sheet['data']:
        rowData = range.get('rowData', [])
        if not rowData:
            continue
        offsets = {'row': range.get('startRow', 0),
                   'col': range.get('startColumn', 0)}
        rangeBGs = [default_bg] * offsets['row']
        rangeValues = [''] * offsets['row']
        for row in rowData:
            colData = row['values']
            newBGs = [default_bg] * offsets['col']
            newVals = [''] * offsets['col']
            for col in colData:
                try:
                    newBGs.append(col['effectiveFormat']['backgroundColor'])
                except KeyError:
                    newBGs.append(default_bg) # Shouldn't get called (all cells have a background)
                try:
                    newVals.append(col['formattedValue']) # Always a string if present.
                except KeyError:
                    newVals.append('') # Not all cells have a value.
            rangeBGs.append(newBGs)
            rangeValues.append(newVals)
        dataset.append({'sheetId': sheet['properties']['sheetId'],
                        'sheetName': sheet['properties']['title'],
                        'backgrounds': rangeBGs,
                        'values': rangeValues})
# dataset is now a list with elements that correspond to the requested ranges,
# and contain 0-base row and column indexed arrays of the backgrounds and values.
# One could add logic to pop elements from the ranges if the entire row has no values.
# Color in A1 of 1st range:
r1 = dataset[0]
print(f'Cell A1 color is {r1["backgrounds"][0][0]} and has value {r1["values"][0][0]}')
print(f'Cell D2 color is {r1["backgrounds"][3][1]} and has value {r1["values"][3][1]}')