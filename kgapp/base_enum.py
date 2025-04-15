from enum import Enum, unique

@unique
class RuleContentTypeEnum(Enum):
    root = 0
    attr = 1
    condition = 2
    action = 3


@unique
class AttributeValueTypeEnum(Enum):
    int = 0
    string = 1
    boolean = 2

RuleContentConnectList = ['&', '|']
RuleContentConnectEnum = Enum('RuleContentConnectEnum', ('&', '|'))


RuleStatusList = ['0', '1']
RuleStatusEnum = Enum('RuleStatusEnum', ('0', '1'))


RuleContentOperatorList = ['=', '>', '>=', '<', '<=']
RuleContentOperatorEnum = Enum('RuleContentOperatorEnum', ('=', '>', '>=', '<', '<='))

RuleContentJudgeTypeList = ['input', 'select']
RuleContentJudgeTypeEnum = Enum('RuleContentJudgeTypeEnum', ('input', 'select'))

AttributeTypeList = ['1', '2']
AttributeTypeEnum = Enum('AttributeTypeEnum', ('1', '2'))