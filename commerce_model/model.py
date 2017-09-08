from enum import Enum

from mesa import Agent, Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation


def compute_offline_retailer_num(model):
    """ Compute the number of Offline Retailer Agents after every step. """
    pass


def compute_online_retailer_num(model):
    """ Compute the number of Online Retailer Agents after every step. """
    pass


def compute_platform_e_commerce_num(model):
    """ Compute the number of E-Commerce Platform Agents after every step."""
    pass


def compute_settled_shop_num(model):
    """ Compute the number of Shops Agent which are settled in E-Commerce Platform Agents after every step. """
    pass


class CommerceModel(Model):
    """
    A simple model of an E-Commerce where Consumer agent, Company(include Offline Retailer,
    Online Retailer, Platform E-commerce, Settled Shop) Agent compete with each other.
    """

    def __init__(self, num_consumer_agents=50, num_category_agents=100, num_offline_retailer_agents=100,
                 num_online_retailer_agents=90, num_platform_e_commerce_agents=40, num_settled_shop_agents=200):
        self.num_consumer_agents = num_consumer_agents
        self.num_category_agents = num_category_agents
        self.num_offline_retailer_agents = num_offline_retailer_agents
        self.num_online_retailer_agents = num_online_retailer_agents
        self.num_platform_e_commerce_agents = num_platform_e_commerce_agents
        self.num_settled_shop_agents = num_settled_shop_agents
        self.running = True
        self.category_schedule = RandomActivation(self)
        self.consumer_schedule = RandomActivation(self)
        self.offline_retailer_schedule = RandomActivation(self)
        self.online_retailer_schedule = RandomActivation(self)
        self.platform_e_commerce_schedule = RandomActivation(self)
        self.settled_shop_schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            model_reporters={
                "num_offline_retailer_agents": compute_offline_retailer_num,
                "num_online_retailer_agents": compute_online_retailer_num,
                "num_platform_e_commerce_agents": compute_platform_e_commerce_num,
                "num_settled_shop_agents": compute_settled_shop_num
            },
            agent_reporters={"": ""}
        )

    def step(self):
        print("step...")

    def run_model(self):
        print("run model...")


class ConsumerAgent(Agent):
    """ An agent with no limited wealth. """
    price_sensitivity = 0
    social_economic_negative_factor = 0
    quality_sensitivity = 0
    social_economic_positive_factor = 0
    advertise_sensitivity = 0
    herd_sensitivity = 0
    variety_sensitivity = 0
    offline_experience_factor = 0

    def __init__(self, unique_id, model, price_sensitivity, social_economic_negative_factor,
                 quality_sensitivity, social_economic_positive_factor, advertise_sensitivity,
                 herd_sensitivity, variety_sensitivity, offline_experience_factor):
        """
        parameter list:
            price_sensitivity => 价格敏感度
            social_economic_negative_factor =>社会地位、经济状况负常数
            quality_sensitivity => 质量敏感度
            social_economic_positive_factor => 社会地位、经济状况正常数
            advertise_sensitivity => 广告效应敏感度
            herd_sensitivity => 从众效应敏感度
            variety_sensitivity => 产品种类多样性敏感度
            offline_experience_factor => 产品线下体验的保留效用
        """
        super().__init__(unique_id, model)
        self.price_sensitivity = price_sensitivity
        self.social_economic_negative_factor = social_economic_negative_factor
        self.quality_sensitivity = quality_sensitivity
        self.social_economic_positive_factor = social_economic_positive_factor
        self.advertise_sensitivity = advertise_sensitivity
        self.herd_sensitivity = herd_sensitivity
        self.variety_sensitivity = variety_sensitivity
        self.offline_experience_factor = offline_experience_factor

    def purchase(self, categories):
        """ 根据产品品种选择某产品，并选择一个厂商进行购买行为，
        根据所有厂商的产品参数和消费者敏感系数计算效用函数值，根据效用函数值选择某厂商的产品;
        假设用户资金无限，有足够的购买力

        Args:
            categories: 产品类别序列

        """
        print("describe the behavior of purchasing...")
        pass

    def __compute_utility(self, category, commerce_agent):
        """消费者效用函数计算，输入category和厂商代理，根据厂商对应的product参数和该消费者敏感系数计算效用。

        Args:
            category: 产品类别
            commerce_agent: 厂商代理

        """
        pass



    def step(self):
        print("step...")


class Category(Agent):
    """
    Product Category Entity
    """
    high_quality = 10
    low_quality = 1
    high_cost = 100
    low_cost = 20
    e_commerce_agents = []

    def __init__(self, unique_id, model, agents=[], high_quality=10, low_quality=1, high_cost=100, low_cost=20):
        super().__init__(unique_id, model)
        self.high_quality = high_quality
        self.low_quality = low_quality
        self.high_cost = high_cost
        self.low_cost = low_cost
        self.e_commerce_agents = agents

    def add_commerce_agent(self, agent):
        """ When an E-Commerce Agent purchases products belong to the Category,
        add an E-Commerce Agent to the Category.

        Args:
            agent: An E-Commerce Agent to be added to the Category.

        """
        self.e_commerce_agents.append(agent)

    def remove_commerce_agent(self, agent):
        """ Remove all instances of a given agent from the Category.

        Args:
            agent: An E-Commerce Agent to be removed from the Category.

        """
        while agent in self.e_commerce_agents:
            self.e_commerce_agents.remove(agent)

    def get_commence_agent_count(self):
        """ Returns the current number of E-Commerce Agents. """
        return len(self.e_commerce_agents)


class Product(object):
    """
    Product Entity
    """

    def __init__(self, category, product_num, product_price, product_cost, product_quality,
                 tax_cost, purchase_cost, sales_cost, logistics_cost):
        """
           Parameter List:
           category => Category类的实例，产品种类表示
           product_num => 产品数量(产销平衡情况下，销量=产量=数量)
           product_price => 产品价格
           product_quality => 产品质量
           tax_cost => 单位产品的税收成本
           purchase_cost => 单位产品的采购成本
           sales_cost => 单位产品的销售成本
           logistics_cost => 单位产品的物流成本
        """
        self.category = category
        self.product_num = product_num
        self.product_price = product_price
        self.product_cost = product_cost
        self.product_quality = product_quality
        self.tax_cost = tax_cost
        self.purchase_cost = purchase_cost
        self.sales_cost = sales_cost
        self.logistics_cost = logistics_cost


class CommerceType(Enum):
    offline_retailer = 1
    online_retailer = 2
    platform_commerce = 3
    settled_shop = 4


class ECommerceAgent(Agent):
    """
    The ECommerce Agent as the parent class, which contains manny all shared attributes.
    """
    rental_cost = 100
    technical_cost = 100
    subsidy_cost = 70
    total_cost = 0
    total_income = 0
    products = []
    is_active = True
    commerce_type = CommerceType.offline_retailer

    def __init__(self, unique_id, model, commerce_type = CommerceType.offline_retailer,
                 rental_cost=100, technical_cost=100, subsidy_cost=70, products=[]):
        """ E-Commerce Agent, as the parent class of Offline Retailer Agent,
        Online Retailer Agent, Platform E-Commerce Agent such as Jingdong, Settled Shop Agent.

            Parameter List:
            rental_cost => 租金成本
            technical_cost => 技术成本
            subsidy_cost => 平台点上对Settled Shops的补贴
        """
        super().__init__(unique_id, model)
        self.commerce_type = commerce_type
        self.rental_cost = rental_cost
        self.technical_cost = technical_cost
        self.subsidy_cost = subsidy_cost
        self.products = products
        self.is_active = True

    def step(self):
        print("step...")

    def add_product(self, product):
        """ When E-Commerce Agent purchases a kind of product, add the product to the products queue. """
        self.products.append(product)

    def remove_product(self, product):
        """ Remove an kind of product from the products queue"""
        while product in self.products:
            self.products.remove(product)

    def get_product_count(self):
        """ Return the current number of products in the queue. """
        return len(self.products)

    def get_commerce_type(self):
        if isinstance(self, OfflineRetailerAgent):
            self.commerce_type = CommerceType.offline_retailer
            return CommerceType.offline_retailer
        elif isinstance(self, OnlineRetailerAgent):
            self.commerce_type = CommerceType.online_retailer
            return CommerceType.online_retailer
        elif isinstance(self, PlatformECommerceAgent):
            self.commerce_type = CommerceType.platform_commerce
            return CommerceType.platform_commerce
        elif isinstance(self, SettledShopAgent):
            return CommerceType.settled_shop

    def purchase(self, categories):
        """ 采购产品，从产品品种中随机选择某个产品，随即选择高质量或低质量;
        假设产销平衡，根据销量决定采购数量;
        确定产品的销售成本和物流成本;
        将该 ECommerceAgent对象增加入指定Category所对应的Agent队列中。

        Args:
            categories: 产品品种列表

        """
        pass

    def __sales_cost(self, category, product):
        """确定某一Category下的产品的单位销售成本"""
        pass

    def __logistics_cost(self, category, product):
        """确定某一Category下的产品的单位物流成本"""
        pass

    def rental_cost(self):
        """计算确定租金成本"""
        pass

    def technical_cost(self):
        """计算确定技术成本"""
        pass

    def subsidy_cost(self):
        """计算确定补贴成本"""
        pass

    def compute_total_cost(self):
        """计算总成本"""
        pass

    def sell_product(self, category, product):
        """当消费者购买该product时，product的销量+1,并计算更新总收入"""
        pass

    def get_products_by_category(self, category):
        """根据Category返回对应的product列表"""
        pass

    def make_decision(self, offline_retailers, online_retailers, platform_agents, settled_agents):
        """在进行一轮销售环节后，计算总成本、总收入、利润，根据市场推出规则确定转变策略,
        从一种类型转为另一种类型;

        """
        pass

    def drop_out(self):
        self.is_active=False


class OfflineRetailerAgent(ECommerceAgent):
    """
    The Offline Retailer Agent, as the child class of ECommerce Agent.
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        print("step...")


class OnlineRetailerAgent(ECommerceAgent):
    """
    The Online REtailer Agent, as the child class of ECommerce Agent.
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        print("step...")


class PlatformECommerceAgent(ECommerceAgent):
    """
    The Platform E-Commerce Agent such as Jingdong, as the child class of ECommerce Agent.
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        print("step...")


class SettledShopAgent(ECommerceAgent):
    """
    The Settled Shop Agent, which is settled in the E-Commerce Platform Agent,
    as the child class of ECommerce Agent.
    """
    platform_agent = None

    def __init__(self, unique_id, model, platform_e_commerce_agent=None):
        super().__init__(unique_id, model)
        self.platform_agent = platform_e_commerce_agent

    def step(self):
        print("step...")