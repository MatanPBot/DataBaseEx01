# ------------------------------------------------------------------------------------------------
def CheckQuery(i_Query):
    SelectIndex = i_Query.index("SELECT");
    FromIndex = i_Query.index("FROM");
    WhereIndex = i_Query.index("WHERE");
    if (checkAttributes(i_Query[SelectIndex + 6:FromIndex - 1].strip()) == False):
        return False, "Invalid Parsing <attribute_list> failed";
    if (isTableList(i_Query[FromIndex + 4:WhereIndex - 1].strip()) == False):
        return False, "Invalid Parsing <table_list> failed";
    if (checkCondition(i_Query[WhereIndex + 5:].strip(), 0, 0) == False):
        return False, "Invalid Parsing <condition> failed";
    return True, "valid";


# ------------------------------------------------------------------------------------------------
def checkAttributes(i_Attributes):
    if (i_Attributes == "*"):
        return True;
    else:
        if (i_Attributes.find("DISTINCT") != -1):
            lst = i_Attributes.split("DISTINCT")
            i_Attributes = (listToString(lst)).strip()
        return isAttributeList(i_Attributes);


# ------------------------------------------------------------------------------------------------
def isAttributeList(i_AttributeList):
    commaIndex = i_AttributeList.find(",")
    if (commaIndex == -1):
        return isAttribute(i_AttributeList.strip());
    else:
        return isAttribute(i_AttributeList[:commaIndex].strip()) and isAttributeList(i_AttributeList[commaIndex + 1:]);


# ------------------------------------------------------------------------------------------------
def isAttribute(i_Attribute):
    attributeSplitList = i_Attribute.split('.');
    if (len(attributeSplitList) == 1):
        return isCustomerAttrbute(attributeSplitList[0]) or isOrderAttribute(attributeSplitList[0]);
    if (attributeSplitList[0] == "Customers"):
        return isCustomerAttrbute(attributeSplitList[1]);
    elif (attributeSplitList[0] == "Orders"):
        return isOrderAttribute(attributeSplitList[1]);
    else:
        return False;


# ------------------------------------------------------------------------------------------------
def isCustomerAttrbute(i_CustomerAttribute):
    return i_CustomerAttribute == "Name" or i_CustomerAttribute == "Age";


# ------------------------------------------------------------------------------------------------
def isOrderAttribute(i_OrderAttribute):
    return i_OrderAttribute == "Product" or i_OrderAttribute == "CustomerName" or i_OrderAttribute == "Price";


# ------------------------------------------------------------------------------------------------
def checkFromToWhere(i_Tables):
    if (len(i_Tables) != 1):
        return False;
    else:
        tableList = i_Tables[0].split(",");
        return isTableList(tableList)


# ------------------------------------------------------------------------------------------------
def isTableList(i_TableList):
    commaIndex = i_TableList.find(",")
    if (commaIndex == -1):
        return isTable(i_TableList.strip())
    else:
        return isTable((i_TableList[:commaIndex]).strip()) and isTableList(i_TableList[commaIndex + 1:])


# ------------------------------------------------------------------------------------------------
def isTable(table):
    return (table == "Customers") or (table == "Orders");


# ------------------------------------------------------------------------------------------------

def checkCondition(i_Conditions, i_nextIndexToSeachANDFrom, i_nextIndexToSearchORFrom):
    andBool = False;
    orBool = False;
    i = i_Conditions.find("AND", i_nextIndexToSeachANDFrom);
    j = i_Conditions.find("OR", i_nextIndexToSearchORFrom);
    if (i == -1 and j == -1):
        return isSimpleCondition(i_Conditions.strip());
    else:
        if (i != -1):
            andBool = checkCondition(i_Conditions[i + 3:].strip(), i + 3, j) and checkCondition(
                i_Conditions[:i].strip(), 0, j);
        if (j != -1):
            orBool = checkCondition(i_Conditions[:j].strip(), i, 0) and checkCondition(i_Conditions[j + 2:].strip(), i,
                                                                                       j + 2);
    return andBool or orBool;


# --------------------------------------------------------------------------------------------
def isSimpleCondition(i_Condition):
    operator = findOperator(i_Condition);
    if (operator == None):
        return False;
    ConditionList = i_Condition.split(operator);
    leftConst = isConstant(ConditionList[0].strip());
    rightConst = isConstant(ConditionList[1].strip());
    return leftConst and rightConst;


# --------------------------------------------------------------------------------------------
def findOperator(i_Condition):
    index = i_Condition.find("<=");
    if (i_Condition.find("<=") != -1):
        return "<=";
    if (i_Condition.find(">=") != -1):
        return ">=";
    if (i_Condition.find("<>") != -1):
        return "<>";
    if (i_Condition.find("=") != -1):
        return "=";
    if (i_Condition.find(">") != -1):
        return ">";
    if (i_Condition.find("<") != -1):
        return "<";
    return None;


# --------------------------------------------------------------------------------------------
def isConstant(i_Constant):
    if (isAttribute(i_Constant)):
        return True;
    if (isString(i_Constant)):
        return True;
    if (i_Constant.isnumeric()):
        return True;
    return False;


# --------------------------------------------------------------------------------------------
def isString(i_String):
    lastIndex = len(i_String) - 1;

    if (i_String.find(chr(8217)) == 0 and i_String.rfind(chr(8217)) == lastIndex):
        return True;
    if (i_String.find("\'") == 0 and i_String.rfind("\'") == lastIndex):
        return True;
    if (i_String.find("\"") == 0 and i_String.rfind("\"") == lastIndex):
        return True;
    return False;


# --------------------------------------------------------------------------------------------
def listToString(lst):
    str = " "
    return (str.join(lst))


# --------------------------------------------------------------------------------------------
userQuery = input("Please enter the query: ");
ans = CheckQuery(userQuery.replace(";", ""));
print(ans[1])

