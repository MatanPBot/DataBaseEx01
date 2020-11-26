# ------------------------------------------------------------------------------------------------
def CheckQuery(i_Query):
    returnString = "Valid";
    attributesIndex = i_Query.index("SELECT");
    tablesIndex = i_Query.index("FROM");
    conditionsIndex = i_Query.index("WHERE");
    checkTablesAndAttributes = checkTables(i_Query[attributesIndex:tablesIndex], i_Query[tablesIndex:conditionsIndex]);
    checkTablesAndCoditions = checkTables(i_Query[conditionsIndex:], i_Query[tablesIndex:conditionsIndex]);
    checkAtt = checkAttributes(i_Query[attributesIndex + 6:tablesIndex - 1].strip());
    if (checkAttributes(
            i_Query[attributesIndex + 6:tablesIndex - 1].strip()) == False or checkTablesAndAttributes == False):
        returnString = "Invalid Parsing <attribute_list> failed";
    elif (isTableList(i_Query[tablesIndex + 4:conditionsIndex - 1].strip()) == False):
        returnString = "Invalid Parsing <table_list> failed";
    elif (checkCondition(i_Query[conditionsIndex + 5:].strip()) == False or checkTablesAndCoditions == False):
        returnString = "Invalid Parsing <condition> failed";
    return returnString;


# ------------------------------------------------------------------------------------------------
def checkTables(i_Attributes, i_Tables):
    isMatchingAttribute = False;
    if (i_Attributes.find("*") != -1):
        isMatchingAttribute = True;
    if (i_Attributes.find("Customers") != -1 and i_Tables.find("Customers") != -1):
        isMatchingAttribute = True;
    if (i_Attributes.find("Orders") != -1 and i_Tables.find("Orders") != -1):
        isMatchingAttribute = True;
    return isMatchingAttribute;


# ------------------------------------------------------------------------------------------------
def checkAttributes(i_Attributes):
    isAttributes = False;
    if (i_Attributes == "*"):
        isAttributes = True;
    if (i_Attributes.find("DISTINCT") == 0):
        if (i_Attributes[8:].strip() == "*"):
            isAttributes = True;
        else:
            i_Attributes = (i_Attributes[8:].strip());
    return isAttributes or isAttributeList(i_Attributes);


# ------------------------------------------------------------------------------------------------
def isAttributeList(i_AttributeList):
    commaIndex = i_AttributeList.find(",");
    isAttributeListBool = False;
    if (commaIndex == -1):
        isAttributeListBool = isAttribute(i_AttributeList.strip());
    else:
        isAttributeListBool = isAttribute(i_AttributeList[:commaIndex].strip()) and isAttributeList(
            i_AttributeList[commaIndex + 1:]);
    return isAttributeListBool;


# ------------------------------------------------------------------------------------------------
def isAttribute(i_Attribute):
    isAttributeBool = True;
    attributeSplitList = i_Attribute.split('.');
    if (len(attributeSplitList) == 1):
        isAttributeBool = False;
    if (attributeSplitList[0] == "Customers"):
        isAttributeBool = isCustomerAttrbute(attributeSplitList[1]);
    elif (attributeSplitList[0] == "Orders"):
        isAttributeBool = isOrderAttribute(attributeSplitList[1]);
    else:
        isAttributeBool = False;
    return isAttributeBool;


# ------------------------------------------------------------------------------------------------
def isCustomerAttrbute(i_CustomerAttribute):
    return i_CustomerAttribute == "Name" or i_CustomerAttribute == "Age";


# ------------------------------------------------------------------------------------------------
def isOrderAttribute(i_OrderAttribute):
    return i_OrderAttribute == "Product" or i_OrderAttribute == "CustomerName" or i_OrderAttribute == "Price"


# ------------------------------------------------------------------------------------------------
def isTableList(i_TableList):
    isTableListBool = False;
    commaIndex = i_TableList.find(",")
    if (commaIndex == -1):
        isTableListBool = isTable(i_TableList.strip())
    else:
        isTableListBool = isTable((i_TableList[:commaIndex]).strip()) and isTableList(i_TableList[commaIndex + 1:])
    return isTableListBool;


# ------------------------------------------------------------------------------------------------
def isTable(table):
    return (table == "Customers") or (table == "Orders");


# ------------------------------------------------------------------------------------------------
def checkCondition(i_Conditions):
    andBool = False;
    leftAndBool = False;
    rightAndBool = False;
    orBool = False;
    leftOrBool = False;
    rightOrBool = False;
    bracketsBool = False;
    simpleCodntionBool = False;

    firstAndIndex = i_Conditions.find("AND", 0);
    firstOrIndex = i_Conditions.find("OR", 0);

    if (i_Conditions.find('(') == 0 and i_Conditions.rfind(')') == (len(i_Conditions) - 1)):
        bracketsBool = checkCondition(i_Conditions[1: (len(i_Conditions) - 1)]);
    elif ((firstAndIndex == -1 and firstOrIndex == -1)):
        simpleCodntionBool = isSimpleCondition(i_Conditions.strip());
    if (bracketsBool == False and simpleCodntionBool == False):
        while ((andBool == False and orBool == False) and (firstAndIndex != -1 or firstOrIndex != -1)):
            if (firstAndIndex != -1):
                leftAndBool = checkCondition(i_Conditions[:firstAndIndex].strip());
                rightAndBool = checkCondition(i_Conditions[firstAndIndex + 3:].strip());
                andBool = leftAndBool and rightAndBool;
            if (firstOrIndex != -1):
                leftOrBool = checkCondition(i_Conditions[:firstOrIndex].strip());
                rightOrBool = checkCondition(i_Conditions[firstOrIndex + 2:].strip());
                orBool = leftOrBool and rightOrBool;
            firstAndIndex = i_Conditions.find("AND", firstAndIndex + 3);
            firstOrIndex = i_Conditions.find("OR", firstOrIndex + 2);
    return andBool or orBool or bracketsBool or simpleCodntionBool;


# --------------------------------------------------------------------------------------------
def isSimpleCondition(i_Condition):
    isSimpleConditionBool = True;
    operator = findOperator(i_Condition);
    if (operator == None):
        isSimpleConditionBool = False;
    else:
        ConditionList = i_Condition.split(operator);
        leftConst = isConstant(ConditionList[0].strip());
        rightConst = isConstant(ConditionList[1].strip());
        if (leftConst[0] == True and rightConst[0] == True):
            isSimpleConditionBool = (leftConst[1] == rightConst[1]);
        else:
            isSimpleConditionBool = False;
    return isSimpleConditionBool;


# --------------------------------------------------------------------------------------------
def findOperator(i_Condition):
    operator = None;
    if (i_Condition.find("<=") != -1):
        operator = "<=";
    if (i_Condition.find(">=") != -1):
        operator = ">=";
    if (i_Condition.find("<>") != -1):
        operator = "<>";
    if (i_Condition.find("=") != -1):
        operator = "=";
    if (i_Condition.find(">") != -1):
        operator = ">";
    if (i_Condition.find("<") != -1):
        operator = "<";
    return operator;


# --------------------------------------------------------------------------------------------
def isConstant(i_Constant):
    isConstantAndType = [];
    if (isAttribute(i_Constant)):
        isConstantAndType = [True, getAttributeType(i_Constant)];
    elif (isString(i_Constant)):
        isConstantAndType = [True, "STRING"];
    elif (i_Constant.isnumeric()):
        isConstantAndType = [True, "INT"];
    else:
        isConstantAndType = [False, None];
    return isConstantAndType;


# --------------------------------------------------------------------------------------------
def getAttributeType(i_Attribute):
    attributeType = "STRING";
    if (i_Attribute.find("Age") != -1 or i_Attribute.find("Price") != -1):
        attributeType = "INT";
    else:
        attributeType = "STRING";
    return attributeType;


# --------------------------------------------------------------------------------------------
def isString(i_String):
    isStringBool = False;
    lastIndex = len(i_String) - 1;
    if (i_String.find("\'") == 0 and i_String.rfind("\'") == lastIndex):
        isStringBool = True;
    if (i_String.find("\"") == 0 and i_String.rfind("\"") == lastIndex):
        isStringBool = True;
    return isStringBool;


# --------------------------------------------------------------------------------------------
userQuery = input("Please enter the query: ");
ans = CheckQuery(userQuery.replace(";", ""));
print(ans);
