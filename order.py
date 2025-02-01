import csv
import calendar
from datetime import date

def findDay(date):
    d = str(date)
    year, month, day = (int(i) for i in d.split('-')) 
    dayNumber = calendar.weekday(year, month, day)
	
	# Modify days list to start with Sunday as 0
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	
    return days[dayNumber]

def getData():
    data = []
    invoices = []
    date_ = str(date.today())
    year, month, day = (int(i) for i in date_.split('-'))
    yesterday = int(day) - 1
    Date = str(month) + str(yesterday)

    with open('All levels_'+Date+'.csv')as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            data.append(row)

    # with open('Invoices_'+Date+'.csv') as file:
    #     csv_file = csv.DictReader(file)
    #     for row in csv_file:
    #         invoices.append(row)

    return data

def menuPortionFunction():

    menuData = []

    with open('menuPortions - menuPortions.csv')as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            menuData.append(row)

    menuPortions = []

    i = 0 
    length = len(menuData)

    while i < length:
        item = menuData[i]["Item"]
        item2 = item
        ingredients = []
        portions = []
        counts = []
        units = []
        while item == item2:
            ingredient = menuData[i]["Ingredient"]
            portion = menuData[i]["Portion"]
            unit = menuData[i]['Units']
            ingredients.append(ingredient.lower())
            if portion != '':
                portion = float(portion)
            portions.append(portion)
            counts.append(0)
            units.append(unit)
            i+=1
            if i == length:
                  break
            item2 = menuData[i]["Item"]
        menuPortion = {
            "Item" : item.lower(),
            "Ingredients" : ingredients,
            "Portions" : portions,
            "Counts" : counts,
            "Units" : units
            } 
        menuPortions.append(menuPortion)

    return menuPortions
 
def Invoice(inv):
    invoices = []

    length = len(inv)

    i = 0

    while i < length:

        invoice = {
            'Product' : inv[i]['Product'],
            'Item Code' : inv[i]['Item Code'],
            'Qty' : float(inv[i]['Qty']),
            'Price' : inv[i]['Price'],
            'Cost' : float(inv[i]['Line Price']),
            'Pack' : inv[i]['Packaging'],
            'Total' : 0
        }
        invoices.append(invoice)
        
        i += 1
    
    i = 0

    while i < length:

        cost = invoices[i]['Cost']
        invoices[i]['Total'] += cost

        i += 1

    return invoices

def orderGuideFunction():

    orderGuide = []

    with open('driscoll_inventory_program.csv')as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            orderGuide.append(row)

    return orderGuide

def Counts(guide):
    counts = []

    i = 0
    length = len(guide)

    while i < length:

        c = {
                "Item" : guide[i]["Item"].lower().strip(),
                "Count" : 0,
                "Ordered" : 0,
                "Units" : '',
                'Item Code' : guide[i]['Item Code'],
                'Ratio' : float(guide[i]['Ratio'])
            }
        counts.append(c)
        i += 1

    return counts

def counterFunction(menu,data):

    i = 0
    j = 0
    length = len(menu)

    while i < length:
        item = menu[i]['Item']

        t = 0

        for row in data:
            food = ''
            food_ = row['Item, open item']
            food_ = food_.lower()
            food = food_
            menu_ = row['Menu group']
            if '*' in food_:
                food = food_[:-1]
            
            modifier = row['Modifiers, special requests']
            modifier = modifier.lower()
            mod = ''
            x = 1

            if ' on side only' in modifier:
                modifier = modifier[:-13]
            if 'add side ' in modifier:
                modifier = modifier[9:]

            mod = modifier

            match modifier:
                case 'greens':
                    mod = 'side of greens'
                case 'fries':
                    mod = 'side of fries'
                case 'apples/grapes':
                    mod = 'side of fruit'
                case 'buffalo':
                    mod = 'side buffalo'
                    x = 2
                case 'mango habanero':
                    mod = 'side mango habanero'
                    x = 2
                case 'carolina bbq':
                    mod = 'side bbq'
                    x = 2
                case 'korean bbq':
                    mod = 'side korean bbq'
                    x = 2
                case '1/2 buffalo':
                    mod = 'side buffalo'
                case '1/2 mango habanero':
                    mod = 'side mango habanero'
                case '1/2 carolina bbq':
                    mod = 'side bbq'
                case '1/2 korean bbq':
                    mod = 'side korean bbq'
                case 'blue cheese':
                    mod = 'side blue cheese'
                case 'ranch':
                    mod = 'side ranch'
                case 'sub gf bun':
                    mod = 'gf bun'
                case 'sub gf bread':
                    mod = 'side of gluten free bread'
                    x = 2
                case 'add salmon':
                    mod = 'add salmon (side)'
                case 'add chicken':
                    mod = 'add chicken (side)'
            
            t = 0
            
            if item == food and row['Type'] == 'menuItem':
                k = 0
                lengthC = len(menu[i]['Counts'])
                while k < lengthC:
                    t = 0
                    qty = float(row['Qty sold'])
                    t = qty * x
                    menu[i]['Counts'][k] += t
                    k += 1

            elif item == mod and row['Type'] == 'modifier':
                k = 0 
                lengthC = len(menu[i]['Counts'])
                while k < lengthC:
                    t = 0
                    qty = float(row['Qty sold'])
                    if menu_ == 'Greens':
                        if  mod == 'add chopped bacon' or mod == 'add bacon':
                            x = 2
                    t = qty * x
                    menu[i]['Counts'][k] += t
                    k += 1

        i += 1

    return menu

def OrderedCounts (c, inv):

    i = 0
    j = 0
    length = len(c)
    lengthInv = len(inv)

    while i < length:

        ic = c[i]['Item Code']
        j = 0

        while j < lengthInv:

            icInv = inv[j]['Item Code']
            pack = inv[j]['Pack']
            qty = inv[j]['Qty']
            r = c[i]['Ratio']
            t = qty

            if pack == 'LB':
                t = qty / r
            
            else:
                t = qty
            
            if ic == icInv:
                c[i]['Ordered'] += t

            j += 1

        i += 1

    return c

def itemTotals(counts, countList):
    length = len(countList)
    lengthCounts = len(counts)
    i = 0
    j = 0
    k = 0

    while i < length:
        item = countList[i]['Item']
        j = 0

        t = 0

        while j < lengthCounts:
            k = 0
            ingredients = counts[j]['Ingredients']
            qtys = counts[j]['Counts']
            portions = counts[j]['Portions']
            units = counts[j]['Units']

            while k < len(ingredients):
                ingredient = ingredients[k]
                qty = qtys[k]
                portion = portions[k]
                if item == ingredient:
                    total = qty * portion
                    unit = units[k]
                    t += total
                    countList[i]['Count'] = t
                    countList[i]['Units'] = unit
                    
                k += 1

            j += 1

        i += 1


    return countList

def makeTheOrder(guide,totals,d):
    dayPars = ["Monday Pars", "Tuesday Pars", "Wednesday Pars", "Thursday Pars", "Friday Pars", "Saturday Pars", "Sunday Pars"]
    daySpan = 0
    dn = 0
    length = len(guide)
    i = 0
    caseTotal = 0

    match d:
        case 'Monday':
            daySpan = 2
            dn = 0
        case 'Tuesday':
            daySpan = 2
            dn = 1
        case 'Wednesday':
            daySpan = 2
            dn = 2
        case 'Thursday':
            daySpan = 2
            dn = 3
        case 'Friday':
            daySpan = 3
            dn = 4
        case 'Sunday':
            daySpan = 2
            dn = 6

    yesterday = 0
    if dn == 0:
        yesterday = 6
    else:
        yesterday = dn - 1
    
    while i < length:
        x = 1
        case_size = float(guide[i]['Total Qty'])
        unit = totals[i]['Units']

        match unit:
            case 'nwoz':
                x = 16
            case 'qty':
                x = 1
            case 'floz':
                x = 1
            case 'lb':
                x = 1
        c = totals[i]['Count']
        c = c / x
        if case_size != 0:
            cases = c / case_size
            cases = round(cases, 3)
        else:
            cases = c
        totals[i]['Count'] = cases

        i += 1

    i = 0

    while i < length:
        caseTotalStr = guide[i]['Total Qty']
        caseTotal = 0
        if caseTotalStr != '':
            caseTotal = float(caseTotalStr)
        dayPar = 0.0

        yPar = float(guide[i][dayPars[yesterday]])

        j = 0

        while j < daySpan:
            dayPar += float(guide[i][dayPars[dn]])
            if dn == 6:
                dn == 0
            else:
                dn += 1

            j += 1
        
        match d:
            case 'Monday':
                daySpan = 2
                dn = 0
            case 'Tuesday':
                daySpan = 2
                dn = 1
            case 'Wednesday':
                daySpan = 2
                dn = 2
            case 'Thursday':
                daySpan = 2
                dn = 3
            case 'Friday':
                daySpan = 3
                dn = 4
            case 'Sunday':
                daySpan = 2
                dn = 6

        t = totals[i]['Count']
        if caseTotal != 0:
            tc = t / caseTotal
            ti = yPar - tc

        order = dayPar - ti
        order = round(order,0)

        totals[i]['Order'] = order

        i += 1

    return totals

def orderSheet(order):
    file = 'order_sheet.csv'
    header = []
    rows = []
    length = len(order)
    i = 0

    while i < length:
        row = []
        add = True
        if order[i]['Count'] == 0:
            add = False
        for k,v in order[i].items():
            if i == 0:
                if k == 'Count':
                    header.append(k+'(Case)')
                else:
                    header.append(k)
            if add:
                row.append(v)
        if add:
            rows.append(row)
        
        i += 1

    with open(file, 'w')as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        csvwriter.writerows(rows)

    # print(header)
    # print(rows)

# creates the menu portions list
menu = menuPortionFunction() 

# creates the order guide list
guide = orderGuideFunction()

# gets the sales and invoice data
data = getData()

# create the invoice dict list
# invoice = Invoice(invoices)

# getting the day of the week
date_ = findDay(date.today())

# tallies all the menu sales
counts = counterFunction(menu,data)

# creates the list of items for final counts
countList = Counts(guide)

# tallies the totals for each item
totals = itemTotals(counts,countList)

# tallies the ordered product
# totals = OrderedCounts(totals, invoice)

# make the order
order = makeTheOrder(guide,totals,date_)

# create the order sheet
orderSheet(order)


##### make case handling for eggs
##### make case handling for gf buns
##### make case handling for gf bread


# print(totals)
# print(date_)
# print(countList)
# print(counts)
# print(guide)
# print(menu)
# print(data)
# print(order)
# print(invoice)