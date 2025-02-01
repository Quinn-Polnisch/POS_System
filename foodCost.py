import csv
import calendar
from datetime import date

def getData():
    data = []
    invoices = []
    date_ = str(date.today())
    year, month, day = (int(i) for i in date_.split('-'))
    yesterday = int(day) - 1
    Date = str(month) + str(yesterday)

    with open('All levels_week.csv')as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            data.append(row)

    with open('Invoices_week.csv') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            invoices.append(row)
    return data, invoices

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

        price = inv[i]['Price']
        qty = inv[i]['Qty']
        cost = inv[i]['Line Price']
        invoice = {
            'Product' : inv[i]['Product'],
            'Item Code' : inv[i]['Item Code'],
            'Qty' : 0,
            'Price' : 0,
            'Cost' : 0,
            'Pack' : inv[i]['Packaging'],
        }

        if price != '':
            invoice['Price'] = float(price)
        
        if qty != '':
            invoice['Qty'] = float(qty)

        if cost != '':
            invoice['Cost'] = float(cost)

        invoices.append(invoice)

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
                'Units' : '',
                'Item Code' : guide[i]['Item Code'],
                'Item Code ALT' : guide[i]['Item Code ALT'],
                'Ratio' : float(guide[i]['Ratio']),
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
                case 'mango haberno':
                    mod = 'side mango haberno'
                    x = 2
                case 'nashville hot':
                    mod = 'side nashville hot'
                    x = 2
                case 'alabama':
                    mod = 'side alabama'
                    x = 2
                case 'bbq':
                    mod = 'side bbq'
                    x = 2
                case 'asian bbq':
                    mod = 'side asian bbq'
                    x = 2
                case '1/2 buffalo':
                    mod = 'side buffalo'
                case '1/2 mango haberno':
                    mod = 'side mango haberno'
                case '1/2 nashville hot':
                    mod = 'side nashville hot'
                case '1/2 alabama':
                    mod = 'side alabama'
                case '1/2 bbq':
                    mod = 'side bbq'
                case '1/2 asian bbq':
                    mod = 'side asian bbq'
                case 'blue cheese':
                    mod = 'side blue cheese'
                case 'ranch':
                    mod = 'side ranch'
                case 'sub gf bun':
                    mod = 'gf bun'
                case 'sub gf bread':
                    mod = 'side of gluten free bread'
                    x = 2
            
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
        altIc = c[i]['Item Code ALT']
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
            
            if ic == icInv or altIc == icInv:
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

def makeTheOrder(guide,totals):

    length = len(guide)
    i = 0
    
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

    foodc = []

    while i < length:

        prod = totals[i]['Item']
        sold = totals[i]['Count']
        ordered = totals[i]['Ordered']
        dif = ordered - sold
        difference = round(dif, 3)
        food = {
            'Product' : prod,
            'Item Code' : guide[i]['Item Code'],
            'Sold' : sold,
            'Ordered' : ordered,
            'Difference' : difference,
            'Inventory Price' : '$' + str(round(difference * float(guide[i]['Case Cost']), 2))
        }

        foodc.append(food)

        i += 1

    return totals, foodc

def FoodCost(guide, fc, data, invoice):

    length = len(guide)
    lengthD = len(data)
    lengthInv = len(invoice)

    netSales = 0
    netOrdered = 0
    beginInv = 0
    endInv = 0
    foodCost = 0

    i = 0 

    fc2 = []

    while i < length:

        prod = fc[i]['Product']
        inv = fc[i]['Difference']
        sold = fc[i]['Sold']
        ordered = fc[i]['Ordered']
        percent = 0
        
        if ordered != 0:
            p = sold / ordered
            percent = round(p, 2)

        food = {
            'Product' : prod,
            'Item Code' : guide[i]['Item Code'],
            'Percent Sold' : percent,
            'Inventory' : inv,

        }

        fc2.append(food)

        i += 1

    j = 0 

    while j < lengthD:

        type_ = data[j]['Type']
        menu_ = data[j]['Menu']
        mg = data[j]['Menu group']

        if type_ == '' and menu_ == 'All Day Food Menu' and mg == '':
            netSales = data[j]['Net sales']

        j += 1

    k = 0

    while k < lengthInv:

        cost = invoice[k]['Cost']
        netOrdered += cost

        k += 1

    k = 0 

    while k < len(fc):

        inv = fc[k]['Difference']

        if inv < 0:
            binv = inv * -1
            price = float(guide[k]['Case Cost']) * binv
            beginInv += price

        else:
            binv = inv
            price = float(guide[k]['Case Cost']) * binv
            endInv += price
            

        k += 1

    invt = beginInv + netOrdered
    inventory = invt - endInv


    foodCost = round((inventory / float(netSales)) * 100, 2)

    fc3 = {
        'Ordered': '$' + str(netOrdered),
        'Sales' : '$' + str(netSales),
        'Begining Inventory' : '$' + str(round(beginInv, 2)),
        'Ending Inventory' : '$' + str(round(endInv, 2)),
        'Food Cost' : str(foodCost) + '%'
        }

    # print(netOrdered)
    # print(netSales)
    # print(beginInv)
    # print(endInv)
    # print(foodCost)

    return fc2, fc3

def foodCostSheet(fc, fc3):
    file = 'food.csv'
    file3 = 'food_cost.csv'

    with open(file, 'w')as csvfile:
        fieldnames = ['Product', 'Item Code', 'Sold', 'Ordered', 'Difference', 'Inventory Price']
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        csvwriter.writerows(fc)

    with open(file3, 'w')as csvfile:
        fieldnames = ['Ordered', 'Sales', 'Begining Inventory', 'Ending Inventory', 'Food Cost']
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        csvwriter.writerow(fc3)

    # print(header)
    # print(rows)

# creates the menu portions list
menu = menuPortionFunction() 

# creates the order guide list
guide = orderGuideFunction()

# gets the sales and invoice data
data, invoices = getData()

# create the invoice dict list
invoice = Invoice(invoices)

# tallies all the menu sales
counts = counterFunction(menu,data)

# creates the list of items for final counts
countList = Counts(guide)

# tallies the totals for each item
totals = itemTotals(counts,countList)

# tallies the ordered product
totals = OrderedCounts(totals, invoice)

# make the order
order, foodC = makeTheOrder(guide,totals)

FoodC, food_cost = FoodCost(guide, foodC, data, invoice)

# create the order sheet
foodCostSheet(foodC, food_cost)


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
# print(foodC)