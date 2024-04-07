import networkx as nx 
import matplotlib.pyplot as plt
import random
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from resources.models import Node


async def create_tables(engine, base):
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.drop_all)
        await conn.run_sync(base.metadata.create_all)


async def generate_hierarchy(session_maker, total_objects=1000, max_childrens=100):
    async with session_maker() as session:
        session: AsyncSession
        try:
            async with session.begin() as transaction:
                # создадим некое кол-во объектов
                nodes = [Node() for i in range(total_objects)]
                session.add_all(nodes)

                # находим случайное ограниченное кол-во нод без родителя, ставим им случайного родителя
                children_quantity = random.randint(2, max_childrens)
                get_children_query = select(Node).where(Node.parent_id.is_(None)).limit(children_quantity)
                while True:
                    children_result = await session.execute(get_children_query)
                    children = children_result.all()
                    if not children or len(children) == 1:
                        break
                    parent = random.choice(children)[0]
                    ids_to_update: list[int] = [child[0].id for child in children[1:]]
                    update_childrens_query = update(Node).where(Node.id.in_(ids_to_update)).values(parent_id=parent.id)
                    await session.execute(update_childrens_query)
                await transaction.commit()
        except Exception:
            await transaction.rollback()


class GraphVisualization: 
    def __init__(self): 
        self.visual = [] 
          
    def addEdge(self, a, b): 
        temp = [a, b] 
        self.visual.append(temp) 

    def visualize(self): 
        G = nx.Graph() 
        G.add_edges_from(self.visual) 
        nx.draw_networkx(G) 
        plt.show() 



async def vizualize_all(session_maker):
    G = GraphVisualization()
    async with session_maker() as session:
        session: AsyncSession
        nodes: list[tuple[Node]] = (await session.execute(select(Node))).all()
        for node in nodes:
            node = node[0]
            if not all([node.parent_id, node.id]):
                continue
            G.addEdge(node.parent_id, node.id)
    G.visualize()
    input()


async def test_generate_token():
    # keycloak_openid = 
    config_well_known = await keycloak_openid.well_known()
    # auth_url = keycloak_openid.auth_url(
        # redirect_uri="http://127.0.0.0:9092/chel",
        # scope="email",
        # state="your_state_info")
    access_token = await keycloak_openid.token(
        grant_type=['password'],
        username="chel",
        password="keycloak",
        )
