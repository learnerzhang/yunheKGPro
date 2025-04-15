from py2neo import Graph, Node, Relationship, cypher, Path

from yunheKGPro.settings import NEOMODEL_NEO4J_BOLT_URL, NEOMODEL_PASSWORD, NEOMODEL_USERNAME


class Neo4j(object):
    graph = None

    def __init__(self):
        self.graph = Graph(NEOMODEL_NEO4J_BOLT_URL, auth=(NEOMODEL_USERNAME, NEOMODEL_PASSWORD))
        # self.graph = Graph("http://10.4.145.209:7474", auth=("neo4j", "123456"))
        print("create neo4j class ...")

    def runcql(self, cql):
        answer = self.graph.run(cql).data()
        return answer

    def entityLabels(self):
        """ 获取实体类型 """
        sql = "CALL db.labels();"
        answer = self.graph.run(sql).data()
        return answer

    def relationshipTypes(self):
        """ 获取关系类型 """
        # CALL db.relationshipTypes
        sql = "CALL db.relationshipTypes;"
        answer = self.graph.run(sql).data()
        return answer

    def indexRelationship(self, total=50, task_id=None):
        if task_id is not None:
            sql = f"MATCH (p)-[r]->(q) WHERE p.task_id={task_id} and q.task_id={task_id} RETURN p, q, r LIMIT {total};"
        else:
            sql = f"MATCH (p)-[r]->(q) RETURN p, q, r LIMIT {total};"
        answer = self.graph.run(sql).data()
        return answer

    def indexRelationshipCount(self):
        """ 统计关系总数 """
        sql = f"MATCH (p)-[r]-(q) RETURN COUNT(r) AS COUNT;"
        answer = self.graph.run(sql).data()
        return answer

    def getAllNodes(self):
        """ 统计实体总数 """
        sql = f"MATCH (n) RETURN n;"
        answer = self.graph.run(sql).data()
        return answer

    def indexEntityCount(self):
        """ 统计实体总数 """
        sql = f"MATCH (n) RETURN count(*) AS COUNT;"
        answer = self.graph.run(sql).data()
        return answer

    def indexRelationshipPage(self, skip, limit=10, total=100):
        sql = f"MATCH (p)-[r]->(q) RETURN p, q, r SKIP {skip} LIMIT {limit};"
        answer = self.graph.run(sql).data()
        return answer

    def fullLeftLinkEntity(self, value, entityType, task_id=None):
        """
            # result = session.run(f"MATCH (p)-[r]->(q) where q.name Contains '{keyword}' RETURN p, q, r")
            # result = session.run(f"MATCH (p)-[r]->(q) where q.name = '{keyword}' RETURN p, q, r")
            # MATCH (p)-[r:`包含`]->(q)  where p.name Contains  "信息" RETURN p, q
            # MATCH (p)-[r:`包含`]->(q)  where p.name="数字孪生黄浦江文件" RETURN p, q  """
        if entityType and value:
            if task_id is not None:
                sql = f"MATCH (p:{entityType})-[r]->(q) where p.name = '{value}' and q.task_id={task_id} RETURN p, q, r;"
            else:
                sql = f"MATCH (p:{entityType})-[r]->(q) where p.name = '{value}' RETURN p, q, r;"

            answer = self.graph.run(sql).data()
            return answer
        else:
            return []

    def leftlinkEntity(self, value, entityType=None):
        """
            # result = session.run(f"MATCH (p)-[r]->(q) where q.name Contains '{keyword}' RETURN p, q, r")
            # result = session.run(f"MATCH (p)-[r]->(q) where q.name = '{keyword}' RETURN p, q, r")
            # MATCH (p)-[r:`包含`]->(q)  where p.name Contains  "信息" RETURN p, q
            # MATCH (p)-[r:`包含`]->(q)  where p.name="数字孪生黄浦江文件" RETURN p, q  """

        if entityType:
            sql = f"MATCH (p:{entityType})-[r]->(q) where p.name =~ '(?i).*{value}.*' RETURN p, q, r;"
        else:
            sql = f"MATCH (p)-[r]->(q) where p.name =~ '(?i).*{value}.*' RETURN p, q, r;"

        answer = self.graph.run(sql).data()
        return answer

    def rightlinkEntity(self, value, entityType=None):
        """
            # result = session.run(f"MATCH (p)-[r]->(q) where q.name Contains '{keyword}' RETURN p, q, r")
            # result = session.run(f"MATCH (p)-[r]->(q) where q.name = '{keyword}' RETURN p, q, r")
            # MATCH (p)-[r:`包含`]->(q)  where p.name Contains  "信息" RETURN p, q
            # MATCH (p)-[r:`包含`]->(q)  where p.name="数字孪生黄浦江文件" RETURN p, q     """
        if entityType:
            sql = f"MATCH (p)-[r]->(q:{entityType}) where q.name =~ '(?i).*{value}.*' RETURN p, q, r;"
        else:
            sql = f"MATCH (p)-[r]->(q) where q.name =~ '(?i).*{value}.*' RETURN p, q, r;"

        answer = self.graph.run(sql).data()
        return answer

    def fullRelationLinkEntity(self, leftValue, rightValue, relationType, limit=100):
        if relationType:
            if leftValue and rightValue:
                sql = f"MATCH (p)-[r:{relationType}]-(q) where p.name =~ '(?i).*{leftValue}.*' and q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r  LIMIT {limit};"
            elif leftValue:
                sql = f"MATCH (p)-[r:{relationType}]-(q) where p.name =~ '(?i).*{leftValue}.*' RETURN p, q, r  LIMIT {limit};"
            elif rightValue:
                sql = f"MATCH (p)-[r:{relationType}]-(q) where q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r  LIMIT {limit};"
            else:
                sql = f"MATCH (p)-[r:{relationType}]-(q) RETURN p, q, r  LIMIT {limit};"

        else:
            if leftValue and rightValue:
                sql = f"MATCH (p)-[r]-(q) where p.name =~ '(?i).*{leftValue}.*' and q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r  LIMIT {limit};"
            elif leftValue:
                sql = f"MATCH (p)-[r]-(q) where p.name =~ '(?i).*{leftValue}.*' RETURN p, q, r  LIMIT {limit};"
            elif rightValue:
                sql = f"MATCH (p)-[r]-(q) where q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r  LIMIT {limit};"
            else:
                sql = f"MATCH (p)-[r]-(q) RETURN p, q, r  LIMIT {limit};"

        print("fullRelationLinkEntity:", sql)
        answer = self.graph.run(sql).data()
        return answer

    def fullGroupRelationLinkEntity(self, leftValue, leftType, group_relations, limit=100):
        if leftType and leftValue:
            sql = f"MATCH (p:{leftType})-[r]-(q) where type(r) in {group_relations} and p.name =~ '(?i).*{leftValue}.*' RETURN p, q, r  LIMIT {limit};"
        elif leftValue:
            sql = f"MATCH (p)-[r]-(q) where type(r) in {group_relations} and p.name =~ '(?i).*{leftValue}.*' RETURN p, q, r  LIMIT {limit};"
        elif leftType:
            sql = f"MATCH (p:{leftType})-[r]-(q) where type(r) in {group_relations} RETURN p, q, r  LIMIT {limit};"
        else:
            sql = f"MATCH (p)-[r]-(q) where type(r) in {group_relations} RETURN p, q, r  LIMIT {limit};"
        print("fullGroupRelationLinkEntity:", sql)
        answer = self.graph.run(sql).data()
        return answer

    def fullTripleEntity(self, leftValue, leftType, rightValue, rightType, relationType, limit=100, search_type=0):
        if search_type == 1:
            sql = f"MATCH (p)-[r]-(q) where p.name = '{leftValue}' RETURN p, q, r  LIMIT {limit};"
            print("fullRelationLinkEntity:", sql)
            answer = self.graph.run(sql).data()
            return answer

        if relationType:
            if leftValue and rightValue:
                if leftType and rightType:
                    sql = f"MATCH (p:{leftType})-[r:{relationType}]-(q:{rightType}) where p.name =~ '(?i).*{leftValue}.*' and q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r  LIMIT {limit};"
                elif leftType:
                    sql = f"MATCH (p:{leftType})-[r:{relationType}]-(q) where p.name =~ '(?i).*{leftValue}.*' and q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r  LIMIT {limit};"
                elif rightType:
                    sql = f"MATCH (p)-[r:{relationType}]-(q:{rightType}) where p.name =~ '(?i).*{leftValue}.*' and q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r  LIMIT {limit};"
                else:
                    sql = f"MATCH (p)-[r:{relationType}]-(q) where p.name =~ '(?i).*{leftValue}.*' and q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r  LIMIT {limit};"
            elif leftValue:
                if leftType and rightType:
                    sql = f"MATCH (p:{leftType})-[r:{relationType}]-(q:{rightType}) where p.name =~ '(?i).*{leftValue}.*' RETURN p, q, r  LIMIT {limit};"
                elif leftType:
                    sql = f"MATCH (p:{leftType})-[r:{relationType}]-(q) where p.name =~ '(?i).*{leftValue}.*' RETURN p, q, r  LIMIT {limit};"
                elif rightType:
                    sql = f"MATCH (p)-[r:{relationType}]-(q:{rightType}) where p.name =~ '(?i).*{leftValue}.*' RETURN p, q, r  LIMIT {limit};"
                else:
                    sql = f"MATCH (p:)-[r:{relationType}]-(q) where p.name =~ '(?i).*{leftValue}.*' RETURN p, q, r  LIMIT {limit};"
            elif rightValue:
                if leftType and rightType:
                    sql = f"MATCH (p:{leftType})-[r:{relationType}]-(q:{rightType}) where q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r  LIMIT {limit};"
                elif rightType:
                    sql = f"MATCH (p)-[r:{relationType}]-(q:{rightType}) where q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r  LIMIT {limit};"
                elif leftType:
                    sql = f"MATCH (p:{leftType})-[r:{relationType}]-(q) where q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r  LIMIT {limit};"
                else:
                    sql = f"MATCH (p)-[r:{relationType}]-(q) where q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r  LIMIT {limit};"
            else:
                if leftType and rightType:
                    sql = f"MATCH (p:{leftType})-[r:{relationType}]-(q:{rightType}) RETURN p, q, r  LIMIT {limit};"
                elif leftType:
                    sql = f"MATCH (p:{leftType})-[r:{relationType}]-(q) RETURN p, q, r  LIMIT {limit};"
                elif rightType:
                    sql = f"MATCH (p)-[r:{relationType}]-(q:{rightType}) RETURN p, q, r  LIMIT {limit};"
                else:
                    sql = f"MATCH (p)-[r:{relationType}]-(q) RETURN p, q, r  LIMIT {limit};"
        else:
            if leftValue and rightValue:
                if leftType and rightType:
                    sql = f"MATCH (p:{leftType})-[r]-(q:{rightType}) where p.name =~ '(?i).*{leftValue}.*' and q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r  LIMIT {limit};"
                elif leftType:
                    sql = f"MATCH (p:{leftType})-[r]-(q) where p.name =~ '(?i).*{leftValue}.*' and q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r  LIMIT {limit};"
                elif rightType:
                    sql = f"MATCH (p)-[r]-(q:{rightType}) where p.name =~ '(?i).*{leftValue}.*' and q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r  LIMIT {limit};"
                else:
                    sql = f"MATCH (p)-[r]-(q) where p.name =~ '(?i).*{leftValue}.*' and q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r  LIMIT {limit};"
            elif leftValue:
                if leftType and rightType:
                    sql = f"MATCH (p:{leftType})-[r]-(q:{rightType}) where p.name =~ '(?i).*{leftValue}.*' RETURN p, q, r  LIMIT {limit};"
                elif leftType:
                    sql = f"MATCH (p:{leftType})-[r]-(q) where p.name =~ '(?i).*{leftValue}.*' RETURN p, q, r  LIMIT {limit};"
                elif rightType:
                    sql = f"MATCH (p)-[r]-(q:{rightType}) where p.name =~ '(?i).*{leftValue}.*' RETURN p, q, r  LIMIT {limit};"
                else:
                    sql = f"MATCH (p)-[r]-(q) where p.name =~ '(?i).*{leftValue}.*' RETURN p, q, r  LIMIT {limit};"
            elif rightValue:
                if leftType and rightType:
                    sql = f"MATCH (p:{leftType})-[r]-(q:{rightType}) where q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r  LIMIT {limit};"
                elif leftType:
                    sql = f"MATCH (p:{leftType})-[r]-(q) where q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r  LIMIT {limit};"
                elif rightType:
                    sql = f"MATCH (p)-[r]-(q:{rightType}) where q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r  LIMIT {limit};"
                else:
                    sql = f"MATCH (p)-[r]-(q) where q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r  LIMIT {limit};"
            else:
                if leftType and rightType:
                    sql = f"MATCH (p:{leftType})-[r]-(q:{rightType}) RETURN p, q, r  LIMIT {limit};"
                elif leftType:
                    sql = f"MATCH (p:{leftType})-[r]-(q) RETURN p, q, r  LIMIT {limit};"
                elif rightType:
                    sql = f"MATCH (p)-[r]-(q:{rightType}) RETURN p, q, r  LIMIT {limit};"
                else:
                    sql = f"MATCH (p)-[r]-(q) RETURN p, q, r  LIMIT {limit};"
        print("fullRelationLinkEntity:", sql)
        answer = self.graph.run(sql).data()
        return answer

    def fullRelationLinkEntityCount(self, leftValue, rightValue, relationType):
        if relationType:
            if leftValue and rightValue:
                sql = f"MATCH (p)-[r:{relationType}]->(q) where p.name =~ '(?i).*{leftValue}.*' and q.name =~ '(?i).*{rightValue}.*' RETURN COUNT(r) AS COUNT;"
            elif leftValue:
                sql = f"MATCH (p)-[r:{relationType}]->(q) where p.name =~ '(?i).*{leftValue}.*' RETURN COUNT(r) AS COUNT;"
            elif rightValue:
                sql = f"MATCH (p)-[r:{relationType}]->(q) where q.name Contains '{leftValue}' RETURN COUNT(r) AS COUNT;"
            else:
                sql = f"MATCH (p)-[r:{relationType}]->(q) RETURN COUNT(r) AS COUNT;"
        else:
            if leftValue and rightValue:
                sql = f"MATCH (p)-[r]->(q) where p.name =~ '(?i).*{leftValue}.*' and q.name =~ '(?i).*{rightValue}.*' RETURN COUNT(r) AS COUNT;"
            elif leftValue:
                sql = f"MATCH (p)-[r]->(q) where p.name =~ '(?i).*{leftValue}.*' RETURN COUNT(r) AS COUNT;"
            elif rightValue:
                sql = f"MATCH (p)-[r]->(q) where q.name =~ '(?i).*{rightValue}.*' RETURN COUNT(r) AS COUNT;"
            else:
                sql = f"MATCH (p)-[r]->(q) RETURN COUNT(r) AS COUNT;"

        answer = self.graph.run(sql).data()
        return answer

    def fullRelationLinkEntityPage(self, leftValue, rightValue, relationType, skip, limit=100):
        if relationType:
            if leftValue and rightValue:
                sql = f"MATCH (p)-[r:{relationType}]->(q) where p.name =~ '(?i).*{leftValue}.*' and q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r SKIP {skip} LIMIT {limit};"
            elif leftValue:
                sql = f"MATCH (p)-[r:{relationType}]->(q) where p.name =~ '(?i).*{leftValue}.*' RETURN p, q, r SKIP {skip} LIMIT {limit};"
            elif rightValue:
                sql = f"MATCH (p)-[r:{relationType}]->(q) where q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r SKIP {skip} LIMIT {limit};"
            else:
                sql = f"MATCH (p)-[r:{relationType}]->(q) RETURN p, q, r SKIP {skip} LIMIT {limit};"

        else:
            if leftValue and rightValue:
                sql = f"MATCH (p)-[r]->(q) where p.name =~ '(?i).*{leftValue}.*' and q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r SKIP {skip} LIMIT {limit};"
            elif leftValue:
                sql = f"MATCH (p)-[r]->(q) where p.name =~ '(?i).*{leftValue}.*' RETURN p, q, r SKIP {skip} LIMIT {limit};"
            elif rightValue:
                sql = f"MATCH (p)-[r]->(q) where q.name =~ '(?i).*{rightValue}.*' RETURN p, q, r SKIP {skip} LIMIT {limit};"
            else:
                sql = f"MATCH (p)-[r]->(q) RETURN p, q, r SKIP {skip} LIMIT {limit};"

        answer = self.graph.run(sql).data()
        return answer

    def fullLinkEntity(self, value, entityType=None):
        if entityType:
            sql = f"MATCH (p:{entityType})-[r]->(q) where p.name =~ '(?i).*{value}.*' RETURN p, q, r;"
        else:
            sql = f"MATCH (p)-[r]->(q) where p.name =~ '(?i).*{value}.*' or q.name =~ '(?i).*{value}.*' RETURN p, q, r;"
        answer = self.graph.run(sql).data()
        return answer

    def relationEntity(self, value, limit=10):
        sql = f"MATCH (p)-[r]->(q) where p.name = '{value}' or q.name = '{value}' RETURN p, q, r LIMIT {limit};"
        answer = self.graph.run(sql).data()
        return answer

    def searchEntity(self, value=None, entityType=None, limit=100):

        value = value.replace("+", "\\+")
        if entityType and value:
            sql = f"MATCH (p:{entityType}) where p.name =~ '(?i).*{value}.*' RETURN p LIMIT {limit};"
        elif value:
            sql = f"MATCH (p) where p.name =~ '(?i).*{value}.*' RETURN p LIMIT {limit};"
        elif entityType:
            sql = f"MATCH (p:{entityType}) RETURN p LIMIT {limit};"
        else:
            sql = f"MATCH (p) RETURN p LIMIT {limit};"

        print("searchEntity:", sql)
        answer = self.graph.run(sql).data()
        return answer

    def searchEntityCount(self, value, entityType=None, limit=100):

        if entityType and value:
            sql = f"MATCH (p:{entityType}) where p.name =~ '(?i).*{value}.*' RETURN COUNT(p) AS COUNT;"
        elif value:
            sql = f"MATCH (p) wherep.name =~ '(?i).*{value}.*' RETURN COUNT(p) AS COUNT;"
        elif entityType:
            sql = f"MATCH (p:{entityType}) RETURN COUNT(p) AS COUNT;"
        else:
            sql = f"MATCH (p) RETURN COUNT(p) AS COUNT;"
        # if entityType:
        # 	sql = f"MATCH (p:{entityType}) where p.name =~ '(?i).*{value}.*' RETURN COUNT(p) AS COUNT;"
        # else:
        # 	sql = f"MATCH (p) where p.name =~ '(?i).*{value}.*' RETURN COUNT(p) AS COUNT;"
        answer = self.graph.run(sql).data()
        return answer

    def searchEntityPage(self, value, skip, limit=100, entityType=None):
        if entityType and value:
            sql = f"MATCH (p:{entityType}) where p.name =~ '(?i).*{value}.*' RETURN p SKIP {skip} LIMIT {limit};"
        elif value:
            sql = f"MATCH (p) where p.name =~ '(?i).*{value}.*' RETURN p SKIP {skip} LIMIT {limit};"
        elif entityType:
            sql = f"MATCH (p:{entityType}) RETURN p SKIP {skip} LIMIT {limit};"
        else:
            sql = f"MATCH (p) RETURN p SKIP {skip} LIMIT {limit};"

        print("searchEntityPage:", sql)
        answer = self.graph.run(sql).data()
        # if entityType:
        # 	sql = f"MATCH (p:{entityType}) where p.name =~ '(?i).*{value}.*' RETURN p SKIP {skip} LIMIT {limit};"
        # else:
        # 	sql = f"MATCH (p) where p.name =~ '(?i).*{value}.*'  RETURN p SKIP {skip} LIMIT {limit};"
        # answer = self.graph.run(sql).data()
        return answer

    def fullLinkEntityCount(self, value, entityType=None):
        if entityType:
            sql = f"MATCH (p:{entityType})-[r]->(q) where p.name =~ '(?i).*{value}.*' RETURN COUNT(r) AS COUNT;"
        else:
            sql = f"MATCH (p)-[r]->(q) where p.name =~ '(?i).*{value}.*' or q.name =~ '(?i).*{value}.*' RETURN COUNT(r) AS COUNT;"
        answer = self.graph.run(sql).data()
        return answer

    def fullLinkEntityPage(self, value, skip, limit=10, entityType=None):
        if entityType:
            sql = f"MATCH (p:{entityType})-[r]->(q) where p.name =~ '(?i).*{value}.*' RETURN p, q, r SKIP {skip} LIMIT {limit};"
        else:
            sql = f"MATCH (p)-[r]->(q) where p.name =~ '(?i).*{value}.*' or q.name =~ '(?i).*{value}.*' RETURN p, q, r SKIP {skip} LIMIT {limit};"
        answer = self.graph.run(sql).data()
        return answer

    def totalNodeNum(self, task_id=None):
        if task_id is not None:
            sql = f"MATCH (n) WHERE n.task_id={task_id} RETURN count(*) AS COUNT;"
        else:
            sql = "MATCH (n) RETURN count(*) AS COUNT;"
        answer = self.graph.run(sql).data()
        return answer

    def totalLinkNum(self, task_id=None):
        if task_id is not None:
            sql = f"MATCH P=(r)-->(s) WHERE r.task_id={task_id} and s.task_id={task_id} RETURN COUNT(*) AS COUNT;"
        else:
            sql = "MATCH P=()-->() RETURN COUNT(*) AS COUNT;"
        answer = self.graph.run(sql).data()
        return answer

    def createNode(self, name, node_type, task_id):
        name = name.replace("'", "\\'")
        name = name.replace('"', '\\"')

        sql = "CREATE (n:" + node_type + " {name: '" + name + "', task_id: " + str(task_id) + "});"
        answer = self.graph.run(sql).data()
        return answer

    def reNameNode(self, nodeid, name):
        sql = f"MATCH (n) WHERE id(n)={nodeid} set n.name = '{name}' RETURN n;"
        answer = self.graph.run(sql).data()
        return answer

    def reNameNodeByName(self, oldname, oldtype, name):
        if oldtype is not None:
            sql = f"MATCH (n:{oldtype}) WHERE n.name='{oldname}' set n.name = '{name}' RETURN n;"
        else:
            sql = f"MATCH (n) WHERE n.name='{oldname}' set n.name = '{name}' RETURN n;"

        answer = self.graph.run(sql).data()
        return answer


    def searchNodeById(self, nodeid):
        sql = f"MATCH (n) WHERE id(n)={nodeid} RETURN n;"
        answer = self.graph.run(sql).data()
        print("searchNodeById:", sql)
        return answer

    def searchNodeRelationById(self, nodeid, limit=1000):
        sql = f"MATCH (p)-[r]-(q) WHERE id(p)={nodeid} RETURN p, q, r LIMIT {limit};"
        answer = self.graph.run(sql).data()
        print("searchNodeRelationById:", sql)
        return answer

    def searchNode(self, name, node_type, task_id):
        name = name.replace("'", "\\'")
        name = name.replace('"', '\\"')

        sql = f"MATCH (n:{node_type}) where n.name='{name}' and n.task_id={task_id} RETURN n;"
        print("searchNode:", sql)
        answer = self.graph.run(sql).data()

        return answer

    def getUseFeatures(self, key, limit=12):
        sql = f"MATCH (p)-[r:使用特征]->(q) where p.name Contains '{key}' RETURN p, q, r LIMIT {limit}; "
        print("getUseFeatures:", sql)
        answer = self.graph.run(sql).data()
        return answer

    def getHasFeatures(self, key, limit=12):
        sql = f"MATCH (p)-[r:具有特征]->(q) where p.name Contains '{key}' RETURN p, q, r LIMIT {limit};"
        print("getHasFeatures:", sql)
        answer = self.graph.run(sql).data()
        return answer

    def getHasYCFeatures(self, key, limit=12):
        sql = f"MATCH (p)-[r:异常类型]->(q) where p.name Contains '{key}' RETURN p, q, r LIMIT {limit};"
        print("getHasFeatures:", sql)
        answer = self.graph.run(sql).data()
        return answer

    def getHasYCMethods(self, key, limit=12):
        sql = f"MATCH (p)-[r:异常类型]->(q) where p.name Contains '{key}' RETURN p, q, r LIMIT {limit};"
        print("getHasFeatures:", sql)
        answer = self.graph.run(sql).data()
        return answer

    def getAppCases(self, key, limit=12):
        sql = f"MATCH (p)-[r:应用案例]->(q) where p.name Contains '{key}' RETURN p, q, r LIMIT {limit};"
        print("getHasFeatures:", sql)
        answer = self.graph.run(sql).data()
        return answer

    def getDocFrom(self, key, limit=12):
        sql = f"MATCH (p)-[r:来源]->(q) where p.name Contains '{key}' RETURN p, q, r LIMIT {limit};"
        print("getDocFrom:", sql)
        answer = self.graph.run(sql).data()
        return answer

    def getFeatType(self, key, limit=12):
        sql = f"MATCH (p:特征类型)-[r:包含]->(q:遥感特征) where q.name Contains '{key}' RETURN p, q, r LIMIT {limit};"
        print("getDocFrom:", sql)
        answer = self.graph.run(sql).data()
        return answer

    def getDatas(self, key, limit=12):
        sql = f"MATCH (p)-[r:使用数据]->(q) where p.name Contains '{key}' RETURN p, q, r LIMIT {limit};"
        print("getDatas:", sql)
        answer = self.graph.run(sql).data()
        return answer

    def deleteAll(self):
        sql = f"MATCH (r) DETACH DELETE r"
        print("delNode:", sql)
        answer = self.graph.run(sql).data()
        return answer

    def deleteTaskAll(self, task_id):
        if task_id is not None:
            sql = f"MATCH (r) where r.task_id={task_id} DETACH DELETE r"
            print("delNode:", sql)
            answer = self.graph.run(sql).data()
        return answer

    def delNode(self, nodeid):
        sql = f"MATCH (r) WHERE id(r) = {nodeid} DETACH DELETE r"
        print("delNode:", sql)
        answer = self.graph.run(sql).data()
        return answer

    def delRelation(self, rel_id):
        sql = f"MATCH ()-[r]-() WHERE id(r) = {rel_id} DELETE r"
        print("delNode:", sql)
        answer = self.graph.run(sql).data()
        return answer

    def delNodeAndRelation(self, name, node_type):
        name = str(name)
        node_type = str(node_type)
        sql = "MATCH (n:" + node_type + "{name:'" + name + "'}) DETACH DELETE (n);"
        print("delNodeAndRelation:", sql)
        answer = self.graph.run(sql).data()
        return answer

    def searchNodeRelationNode(self, name1, name2, rel_type, name_type1=None, name_type2=None, task_id=None):
        name1 = str(name1)
        name2 = str(name2)

        name1 = name1.replace("'", "\\'")
        name1 = name1.replace('"', '\\"')

        name2 = name2.replace("'", "\\'")
        name2 = name2.replace('"', '\\"')

        rel_type = str(rel_type)
        name_type1 = str(name_type1) if name_type1 is not None else None
        name_type2 = str(name_type2) if name_type2 is not None else None

        if name_type1 and name_type2 and task_id:
            sql = f"MATCH (p:{name_type1}) - [r:{rel_type}] -> (q:{name_type2})  WHERE p.name = '{name1}' and q.name = '{name2}' and p.task_id = {task_id} and q.task_id = {task_id} RETURN p, q, r;"
        elif name_type1:
            sql = f"MATCH (p:{name_type1}) - [r:{rel_type}] -> (q)  WHERE p.name = '{name1}' and q.name = '{name2}'  RETURN p, q, r;"
        elif name_type2:
            sql = f"MATCH (p) - [r:{rel_type}] -> (q:{name_type2})  WHERE p.name = '{name1}' and q.name = '{name2}'  RETURN p, q, r;"
        else:
            sql = f"MATCH (p) - [r:{rel_type}] -> (q)  WHERE p.name = '{name1}' and q.name = '{name2}'  RETURN p, q, r;"
        answer = self.graph.run(sql).data()
        print("searchNodeRelationNode:", sql)
        return answer

    def createNodeRelationByIds(self, fromNodeId, rel_type, toNodeId):
        # MATCH (x) , (y), (r: rel_type) where id(x)==fromNodeId AND id(y)==toNodeId create (x) - [r] -> (y)
        sql = f"MATCH (p), (q) where id(p) = {fromNodeId} and id(q) = {toNodeId} create (p) - [r:{rel_type}] -> (q) RETURN p, q, r;"
        print("createNodeRelationByIds", sql)
        answer = self.graph.run(sql).data()
        return answer

    def createNodeRelationNode(self, name1, name2, rel_type, name_type1=None, name_type2=None, task_id=None):
        # MATCH (x {name:'name1'}) , (y {name:'name2'}), (r: rel_type)  create (x) - [r] -> (y)
        name1 = str(name1)
        name2 = str(name2)

        name1 = name1.replace("'", "\\'").replace('"', '\\"')

        name2 = name2.replace("'", "\\'").replace('"', '\\"')

        rel_type = str(rel_type)
        name_type1 = str(name_type1) if name_type1 else None
        name_type2 = str(name_type2) if name_type2 else None

        if name_type1 and name_type2:
            sql = "MATCH (p:" + name_type1 + " {name:'" + name1 + "', task_id: " + str(task_id) + "}), (q:" + name_type2 + " {name:'" + name2 + "', task_id: " + str(task_id) + "})  create (p) - [r:" + rel_type + "] -> (q) RETURN p, q, r;"
        elif name_type1:
            sql = "MATCH (p:" + name_type1 + " {name:'" + name1 + "', task_id: " + str(task_id) + "}), (q {name:'" + name2 + "', task_id: " + str(task_id) + "})  create (p) - [r:" + rel_type + "] -> (q) RETURN p, q, r;"
        elif name_type2:
            sql = "MATCH (p {name:'" + name1 + "', task_id: " + str(task_id) + "}), (q:" + name_type2 + " {name:'" + name2 + "', task_id: " + str(task_id) + "})  create (p) - [r:" + rel_type + "] -> (q) RETURN p, q, r;"
        else:
            sql = "MATCH (p {name:'" + name1 + "', task_id: " + str(task_id) + "}), (q {name:'" + name2 + "', task_id: " + str(task_id) + "})  create (p) - [r:" + rel_type + "] -> (q) RETURN p, q, r;"
        print("createNodeRelationNode", sql)
        answer = self.graph.run(sql).data()
        return answer

    def matchItembyTitle(self, value):

        sql = "MATCH (n:Item { title: '" + str(value) + "' }) return n;"
        answer = self.graph.run(sql).data()
        return answer

    def matchEntityByName(self, value):
        sql = f"MATCH (n) WHERE n.name = '{value}' return n;"
        try:
            answer = self.graph.run(sql).data()
        except:
            print(sql)
        return answer

    # 根据title值返回互动百科item
    def matchHudongItembyTitle(self, value):
        sql = "MATCH (n:HudongItem { title: '" + str(value) + "' }) return n;"
        try:
            answer = self.graph.run(sql).data()
        except:
            print(sql)
        return answer

    # 根据entity的名称返回关系
    def getEntityRelationbyEntity(self, value):
        answer = self.graph.run("MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.title = \"" + str(
            value) + "\" RETURN rel,entity2").data()
        return answer

    # 查找entity1及其对应的关系（与getEntityRelationbyEntity的差别就是返回值不一样）
    def findRelationByEntity(self, entity1):
        answer = self.graph.run("MATCH (n1 {title:\"" + str(entity1) + "\"})- [rel] -> (n2) RETURN n1,rel,n2").data()
        # if(answer is None):
        # 	answer = self.graph.run("MATCH (n1:NewNode {title:\""+entity1+"\"})- [rel] -> (n2) RETURN n1,rel,n2" ).data()
        return answer

    # 查找entity2及其对应的关系
    def findRelationByEntity2(self, entity1):
        answer = self.graph.run("MATCH (n1)- [rel] -> (n2 {title:\"" + str(entity1) + "\"}) RETURN n1,rel,n2").data()
        # if(answer is None):
        # 	answer = self.graph.run("MATCH (n1)- [rel] -> (n2:NewNode {title:\""+entity1+"\"}) RETURN n1,rel,n2" ).data()
        return answer

    # 根据entity1和关系查找enitty2
    def findOtherEntities(self, entity, relation):
        answer = self.graph.run("MATCH (n1 {title:\"" + str(entity) + "\"})- [rel {type:\"" + str(
            relation) + "\"}] -> (n2) RETURN n1,rel,n2").data()
        # if(answer is None):
        #	answer = self.graph.run("MATCH (n1:NewNode {title:\"" + entity + "\"})- [rel:RELATION {type:\""+relation+"\"}] -> (n2) RETURN n1,rel,n2" ).data()

        return answer

    # 根据entity2和关系查找enitty1
    def findOtherEntities2(self, entity, relation):
        answer = self.graph.run("MATCH (n1)- [rel {type:\"" + str(relation) + "\"}] -> (n2 {title:\"" + str(
            entity) + "\"}) RETURN n1,rel,n2").data()
        # if(answer is None):
        #	answer = self.graph.run("MATCH (n1)- [rel:RELATION {type:\""+relation+"\"}] -> (n2:NewNode {title:\"" + entity + "\"}) RETURN n1,rel,n2" ).data()

        return answer

    # 根据两个实体查询它们之间的最短路径
    def findRelationByEntities(self, entity1, entity2):
        answer = self.graph.run("MATCH (p1:HudongItem {title:\"" + str(entity1) + "\"}),(p2:HudongItem{title:\"" + str(
            entity2) + "\"}),p=shortestpath((p1)-[rel:RELATION*]-(p2)) RETURN rel").evaluate()
        # answer = self.graph.run("MATCH (p1:HudongItem {title:\"" + entity1 + "\"})-[rel:RELATION]-(p2:HudongItem{title:\""+entity2+"\"}) RETURN p1,p2").data()

        if (answer is None):
            answer = self.graph.run(
                "MATCH (p1:HudongItem {title:\"" + str(entity1) + "\"}),(p2:NewNode {title:\"" + str(
                    entity2) + "\"}),p=shortestpath((p1)-[rel:RELATION*]-(p2)) RETURN p").evaluate()
        if (answer is None):
            answer = self.graph.run("MATCH (p1:NewNode {title:\"" + str(entity1) + "\"}),(p2:HudongItem{title:\"" + str(
                entity2) + "\"}),p=shortestpath((p1)-[rel:RELATION*]-(p2)) RETURN p").evaluate()
        if (answer is None):
            answer = self.graph.run("MATCH (p1:NewNode {title:\"" + str(entity1) + "\"}),(p2:NewNode {title:\"" + str(
                entity2) + "\"}),p=shortestpath((p1)-[rel:RELATION*]-(p2)) RETURN p").evaluate()
        # answer = self.graph.data("MATCH (n1:HudongItem {title:\"" + entity1 + "\"})- [rel] -> (n2:HudongItem{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
        # if(answer is None):
        #	answer = self.graph.data("MATCH (n1:HudongItem {title:\"" + entity1 + "\"})- [rel] -> (n2:NewNode{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
        # if(answer is None):
        #	answer = self.graph.data("MATCH (n1:NewNode {title:\"" + entity1 + "\"})- [rel] -> (n2:HudongItem{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
        # if(answer is None):
        #	answer = self.graph.data("MATCH (n1:NewNode {title:\"" + entity1 + "\"})- [rel] -> (n2:NewNode{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
        relationDict = []
        if (answer is not None):
            for x in answer:
                tmp = {}
                start_node = x.start_node
                end_node = x.end_node
                tmp['n1'] = start_node
                tmp['n2'] = end_node
                tmp['rel'] = x
                relationDict.append(tmp)
        return relationDict

    # 查询数据库中是否有对应的实体-关系匹配
    def findEntityRelation(self, entity1, relation, entity2):
        answer = self.graph.run("MATCH (n1:HudongItem {title:\"" + str(entity1) + "\"})- [rel:RELATION {type:\"" + str(
            relation) + "\"}] -> (n2:HudongItem{title:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        if (answer is None):
            answer = self.graph.run(
                "MATCH (n1:HudongItem {title:\"" + str(entity1) + "\"})- [rel:RELATION {type:\"" + str(
                    relation) + "\"}] -> (n2:NewNode{title:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        if (answer is None):
            answer = self.graph.run("MATCH (n1:NewNode {title:\"" + str(entity1) + "\"})- [rel:RELATION {type:\"" + str(
                relation) + "\"}] -> (n2:HudongItem{title:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        if (answer is None):
            answer = self.graph.run("MATCH (n1:NewNode {title:\"" + str(entity1) + "\"})- [rel:RELATION {type:\"" + str(
                relation) + "\"}] -> (n2:NewNode{title:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        return answer


if __name__ == '__main__':
    npy = Neo4j()
    rt = npy.relationshipTypes()
    print(rt)

    rt = npy.searchNode(name="zz", node_type="abc")
    print(rt)

    rt = npy.searchNodeRelationNode(name1="tmpname", name_type1="tmptype", rel_type="relname", name2="toEntname", name_type2="toEnttype")
    print(rt)
    # npy.searchNode()

    pass
