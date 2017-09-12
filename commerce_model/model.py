from enum import Enum
from random import choice, random

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


def get_last_agent_id_from_schedule(schedule):
    """ Return the last agent id from model.schedule."""
    if schedule is not None:
        agent_len = len(schedule.agents)
        last_agent = schedule.agents[agent_len - 1]
        items = last_agent.unique_id.split('_')
        return items[len(items) -1]
    return None


class CommerceModel(Model):
    """
    A simple model of an E-Commerce where Consumer agent, Company(include Offline Retailer,
    Online Retailer, Platform E-commerce, Settled Shop) Agent compete with each other.
    """
    model_type = "China"   # China or American
    product_quality_list = [ProductQuality.low_quality, ProductQuality.high_quality]

    offline_retailer_policy = [CommerceType.offline_retailer, CommerceType.online_retailer, CommerceType.settled_shop]
    online_retailer_policy = [CommerceType.online_retailer, CommerceType.settled_shop]
    settled_shop_policy = [CommerceType.platform_commerce, CommerceType.online_retailer, CommerceType.offline_retailer]

    def __init__(self, model_type="China", num_consumer_agents=50, num_category_agents=100, num_offline_retailer_agents=100,
                 num_online_retailer_agents=90, num_platform_e_commerce_agents=40, num_settled_shop_agents=200):
        self.model_type = model_type
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

        # Init the Agents List
        self.__init_category_agents(self.num_consumer_agents)
        self.__init_consumer_agents(self.num_consumer_agents)
        self.__init_offline_retailer_agents(self.num_offline_retailer_agents)
        self.__init_online_retailer_agents(self.num_online_retailer_agents)
        self.__init_platform_e_commerce_agents(self.num_platform_e_commerce_agents)
        self.__init_settled_shop_agents(self.num_settled_shop_agents)

    def __init_consumer_agents(self, num_consumer_agents):
        """ Init the Consumer Agent List"""
        for i in range(num_consumer_agents):
            unique_id = "consumer" + i
            price_sensitivity = 10
            social_economic_negative_factor = -8
            quality_sensitivity = 4
            social_economic_positive_factor = 8
            advertise_sensitivity = 5
            herd_sensitivity = 8
            variety_sensitivity = 8
            offline_experience_factor = 5
            consumer_agent = ConsumerAgent(unique_id, self, price_sensitivity, social_economic_negative_factor,
                                           quality_sensitivity, social_economic_positive_factor, advertise_sensitivity,
                                           herd_sensitivity, variety_sensitivity, offline_experience_factor)
            self.consumer_schedule.add(consumer_agent)

    def __init_category_agents(self, num_category_agents):
        """ Init the Category Agent List"""
        for i in range(num_category_agents):
            unique_id = "category" + i
            agents = []
            high_quality = 10
            low_quality = 1

            # 产品种类高低价格区间
            high_cost = random.randint(50,100)
            low_cost = random.randint(5,25)
            category_agent = CategoryAgent(unique_id, self, agents, high_quality, low_quality, high_cost, low_cost)
            self.category_schedule.add(category_agent)

    def __init_offline_retailer_agents(self, num_offline_retailer_agents):
        """ Init the Offline Retailer Agent List"""
        for i in range(num_offline_retailer_agents):
            unique_id = "offline_retailer_" + i
            rental_cost = 100
            offline_retailer_agent = OfflineRetailerAgent(unique_id, self, CommerceType.offline_retailer, rental_cost)
            self.offline_retailer_schedule.add(offline_retailer_agent)

    def __init_online_retailer_agents(self, num_online_retailer_agents):
        """ Init the Online Retailer Agent List """
        for i in range(num_online_retailer_agents):
            unique_id = "online_retailer_" + i
            technical_cost = 100
            online_retailer_agent = OnlineRetailerAgent(unique_id, self, CommerceType.online_retailer, 0, technical_cost, 0, [])
            self.online_retailer_schedule.add(online_retailer_agent)

    def __init_platform_e_commerce_agents(self, num_platform_e_commerce_agents):
        """ Init the Platform E-Commerce Agent List"""
        for i in range(num_platform_e_commerce_agents):
            unique_id = "platform_e_commerce_" + i
            technical_cost = 200
            subsidy_cost = 80
            platform_e_commerce_agent = PlatformECommerceAgent(unique_id, self, technical_cost, subsidy_cost)
            self.platform_e_commerce_schedule.add(platform_e_commerce_agent)

    def __init_settled_shop_agents(self, num_settled_shop_agents):
        """ Init the Settled Shop Agent List"""
        for i in range(num_settled_shop_agents):
            unique_id = "settled_shop_" + i
            subsidy_cost = 10
            rental_cost = 40 # 入驻平台电商成本
            # 随机选取一个平台电商，作为Settled Shop所依赖的电商平台
            platform_e_commerce_agent = choice(self.platform_e_commerce_schedule.agents)
            settled_shop_agent = SettledShopAgent(unique_id, self, rental_cost, subsidy_cost, platform_e_commerce_agent)
            self.settled_shop_schedule.add(settled_shop_agent)

    def __commerce_purchase(self):
        """ 厂商从产品种类中采购商品 """
        self.__commerce_purchase_products(self.offline_retailer_schedule.agents)
        self.__commerce_purchase_products(self.online_retailer_schedule.agents)
        self.__commerce_purchase_products(self.settled_shop_schedule.agents)

    def __commerce_purchase_products(self, e_commerce_agents):
        """ 厂商从产品种类中采购商品 """
        for e_commerce_agent in e_commerce_agents:
            product_diversity = random.randint(1, 15)
            if product_diversity >= len(self.category_schedule.agents):
                for category_agent in self.category_schedule.agents:
                    self.__generate_product(e_commerce_agent, category_agent)
            else:
                selected_category_agents = random.sample(self.category_schedule.agents, product_diversity)
                for category_agent in selected_category_agents:
                    self.__generate_product(e_commerce_agent, category_agent)

    @classmethod
    def choose_quality(cls):
        return choice(cls.product_quality_list)

    def __generate_product(self, e_commerce_agent, category_agent):
        """ Generate product for E-Commerce Agent and Category Agent"""
        product_num = 0
        # 随机选择高低质量
        quality = CommerceModel.choose_quality()
        if quality == ProductQuality.high_quality:
            product_quality = random.randint(6, 10)
            product_cost = random.randint(category_agent.high_cost - 5, category_agent.high_cost + 5)
        elif quality == ProductQuality.low_quality:
            product_quality = random.randint(1, 5)
            product_cost = random.randint(category_agent.low_cost - 5, category_agent.low_cost + 5)
        tax_cost = product_cost * 0.03  # 假设tax_cost = product_cost * 3%
        product_price = product_cost * (e_commerce_agent.addition_rate + 1)
        sales_cost = product_cost * 0.05  # sales_cost = product_cost * 5%
        logistics_cost = product_cost * 0.04  # logistics_cost = product_cost * 4%
        product = Product(category_agent, product_num, product_price, product_cost, product_quality,
                          tax_cost, sales_cost, logistics_cost)
        e_commerce_agent.add_product(product)
        category_agent.add_commerce_agent(e_commerce_agent)

    def __clear_schedule_agents(self):
        """ After every step, clear the original data and init the params."""
        for offline_retailer in self.offline_retailer_schedule.agents:
            offline_retailer.clear()

        for online_retailer in self.online_retailer_schedule.agents:
            online_retailer.clear()

        for settled_shop in self.settled_shop_schedule.agents:
            settled_shop.clear()

    def step(self):
        self.datacollector.collect(self)
        if self.offline_retailer_schedule.steps > 0:
            self.__clear_schedule_agents()
        # all E-Commerce Agents randomly purchase products from all Category Agents.
        self.__commerce_purchase()
        # all Consumer Agents randomly purchase products from E-Commerce Agents
        self.consumer_schedule.step()
        # After Consumer Agents purchase products, all E-Commerce Agents
        # compute total income and cost, then gain the profit
        self.offline_retailer_schedule.step()
        self.online_retailer_schedule.step()
        self.settled_shop_schedule.step()

    def run_model(self, n):
        for i in range(n):
            self.step()


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

    def __compute_utility(self, product, e_commerce_agent, ave_product_price=0, ave_product_quality=0):
        """消费者效用函数计算，输入category和厂商代理，根据厂商对应的product参数和该消费者敏感系数计算效用。

        Args:
            product: 产品类别
            e_commerce_agent: 厂商代理
            ave_product_price: 产品平均价格 默认值为0
            ave_product_quality: 产品平均质量 默认值为0

        """
        product_diversity = e_commerce_agent.get_product_count()
        utility = (-self.price_sensitivity ** (product.product_price - ave_product_price)
                   + self.social_economic_negative_factor) * product.product_price
        utility += (-self.quality_sensitivity ** (product.product_quality - ave_product_quality)
                    + self.social_economic_positive_factor) * product.product_quality
        utility += self.advertise_sensitivity * product.advertise_effect
        utility += self.herd_sensitivity * product.herd_effect
        utility += self.variety_sensitivity * product_diversity
        utility += self.offline_experience_factor * product.offline_exp_effect
        return utility

    def __compute_utility(self, product_price, ave_product_price, product_quality,
                          ave_product_quality, advertise_effect, herd_effect, product_diversity, offline_exp_effect):
        """ Compute the Utility of Consumer Agent """
        utility = (-self.price_sensitivity**(product_price-ave_product_price)
                   + self.social_economic_negative_factor)*product_price
        utility += (-self.quality_sensitivity**(product_quality-ave_product_quality)
                    +self.social_economic_positive_factor)*product_quality
        utility += self.advertise_sensitivity * advertise_effect
        utility += self.herd_sensitivity * herd_effect
        utility += self.variety_sensitivity * product_diversity
        utility += self.offline_experience_factor * offline_exp_effect
        return utility

    def step(self):
        """When starting a step, the Consumer Agent traversals every Category Agent from Category Agents,
        then choose one E-Commerce Agent from the Category Agent for purchasing product.
        One Category Agent responses to at least one or manny E-Commerce Agents.

        """
        for category_agent in self.model.category_schedule.agents:
            opt_utility = 0
            opt_product = None
            opt_e_commerce_agent = None
            for e_commerce_agent in category_agent.e_commerce_agents:
                products = e_commerce_agent.get_products_by_category(category_agent)
                for product in products:
                    utility = self.__compute_utility(product, e_commerce_agent, 0, 0)
                    if utility > opt_utility:
                        opt_utility = utility
                        opt_product = product
                        opt_e_commerce_agent = e_commerce_agent
            opt_product.product_num += 1


class CategoryAgent(Agent):
    """
    Product Category Entity
    """

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

    def clear_commerce_agents(self):
        self.e_commerce_agents.clear()

    def get_commence_agent_count(self):
        """ Returns the current number of E-Commerce Agents. """
        return len(self.e_commerce_agents)


class Product(object):
    """
    Product Entity
    """

    def __init__(self, category, product_num, product_price, product_cost, product_quality,
                 tax_cost, sales_cost, logistics_cost, advertise_effect=0, herd_effect=0,offline_exp_effect=0):
        """
           Parameter List:
           category => Category类的实例，产品种类表示
           product_num => 产品数量(产销平衡情况下，销量=产量=数量)
           product_price => 产品价格
           product_quality => 产品质量
           tax_cost => 单位产品的税收成本 product_cost * (0.02~0.04之间的随机数,默认0.02)
           product_cost => 单位产品的采购成本
           sales_cost => 单位产品的销售成本 product_cost * (0.03_0.06之间的随机数，默认0.05)
           logistics_cost => 单位产品的物流成本 product_cost * (0.03_0.04之间的随机数，默认0.04)
           advertise_effect => 产品广告效应值，默认值为0
           herd_effect => 产品从众效应值，默认值为0
           offline_exp_effect => 线下体验带来的消费者保留效用值，默认值为0

        """
        self.category = category
        self.product_num = product_num
        self.product_price = product_price
        self.product_cost = product_cost
        self.product_quality = product_quality
        self.tax_cost = tax_cost
        self.sales_cost = sales_cost
        self.logistics_cost = logistics_cost
        self.advertise_effect = advertise_effect
        self.herd_effect = herd_effect
        self.offline_exp_effect = offline_exp_effect


class CommerceType(Enum):
    offline_retailer = 1
    online_retailer = 2
    platform_commerce = 3
    settled_shop = 4


class ProductQuality(Enum):
    high_quality = 1
    low_quality = 2


class ECommerceAgent(Agent):
    """
    The ECommerce Agent as the parent class, which contains manny all shared attributes.
    """

    def __init__(self, unique_id, model, commerce_type = CommerceType.offline_retailer,
                 rental_cost=100, technical_cost=100, subsidy_cost=70, products=[]):
        """ E-Commerce Agent, as the parent class of Offline Retailer Agent,
        Online Retailer Agent, Platform E-Commerce Agent such as Jingdong, Settled Shop Agent.

            Parameter List:
            rental_cost => 租金成本
            technical_cost => 技术成本
            subsidy_cost => 平台点上对Settled Shops的补贴
            addition_rate => 厂商定价时价格加成的加成率
        """
        super().__init__(unique_id, model)
        self.commerce_type = commerce_type
        self.rental_cost = rental_cost
        self.technical_cost = technical_cost
        self.subsidy_cost = subsidy_cost
        self.products = products
        self.total_tax_cost = 0  # 税收成本
        self.total_cost = 0
        self.total_income = 0
        self.total_profit = 0
        self.is_active = True
        self.step_profits = []
        self.addition_rate = ECommerceAgent.compute_addition_rate()

    @classmethod
    def compute_addition_rate(cls):
        addition_rate = round(random.random(), 2)
        addition_rate = addition_rate-0.5 if addition_rate>0.5 else addition_rate
        return addition_rate

    def clear(self):
        """ After every step, clear the original data and init the params."""
        if self.get_product_count() > 0:
            self.products = []
            self.total_cost = 0
            self.total_income = 0
            self.total_profit = 0
            self.total_tax_cost = 0
            self.addition_rate = ECommerceAgent.compute_addition_rate()

    def step(self):
        """After Consumer Agents purchase products, all E-Commerce Agents
           compute total income and cost, then gain the profit.

        """
        # If the products count of the agent is 0, then it is new created agent and need not to
        # compute total income/cost and make decision.
        if self.get_product_count() > 0:
            self.compute_total_cost()
            self.make_decision()

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

    def add_step_profit(self, step_profit):
        """ 记录本轮次(step)的利润，在产销均衡的情况下，总收入-总成本=利润，利润可以为负值"""
        self.step_profits.append(step_profit)

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
        products = self.get_products_by_category(category)
        sales_cost = products[0].product_cost if len(products)>0 else 0
        return sales_cost

    def __logistics_cost(self, category, product):
        """确定某一Category下的产品的单位物流成本"""
        products = self.get_products_by_category(category)
        logistics_cost = products[0].logistics_cost if len(products) > 0 else 0
        return logistics_cost

    def rental_cost(self):
        """计算确定租金成本"""
        return self.rental_cost

    def technical_cost(self):
        """计算确定技术成本"""
        return self.technical_cost

    def subsidy_cost(self):
        """计算确定补贴成本"""
        return self.subsidy_cost

    def compute_total_cost(self):
        """计算总成本"""
        for product in self.products:
            self.total_cost += (product.product_cost + product.sales_cost
                                + product.logistics_cost) * product.product_num
            self.total_tax_cost += product.tax_cost * product.product_num
            self.total_income += product.product_price * product.product_num
        # 总成本
        self.total_cost += self.rental_cost + self.technical_cost + self.subsidy_cost + self.total_tax_cost
        # 总利润
        self.total_profit = self.total_income - self.total_cost
        # 记录本轮销售得到的总利润
        self.add_step_profit(self.total_profit)

    def sell_product(self, category, product):
        """当消费者购买该product时，product的销量+1,并计算更新总收入"""
        pass

    def get_products_by_category(self, category):
        """根据Category返回对应的product列表"""
        products = []
        for product in self.products:
            if product.category.unique_id == category.unique_id:
                products.append(product)
        return products

    def make_decision(self):
        """在进行一轮销售环节后，计算总成本、总收入、利润，根据市场推出规则确定转变策略,
        从一种类型转为另一种类型;

        """
        if self.total_profit > 0:
            print(self.unique_id, "在step", len(self.step_profits), "中盈利!")
        elif self.__is_exit_by_profit():
            # 如果连续三年未盈利，退出市场
            if self.commerce_type == CommerceType.offline_retailer:
                self.model.offline_retailer_schedule.remove(self)
            elif self.commerce_type == CommerceType.online_retailer:
                self.model.online_retailer_schedule.remove(self)
            elif self.commerce_type == CommerceType.settled_shop:
                self.model.settled_shop_schedule.remove(self)
        else:
            # 如果本轮未盈利，且尚未连续三年内亏损，则选择转换平台
            if self.commerce_type == CommerceType.offline_retailer:
                target_commerce_type = choice(CommerceModel.offline_retailer_policy)
                ECommerceAgent.transform_commerce_type(self, target_commerce_type)
                self.model.offline_retailer_schedule.remove(self)
            elif self.commerce_type == CommerceType.online_retailer:
                target_commerce_type = choice(CommerceModel.online_retailer_policy)
                ECommerceAgent.transform_commerce_type(self, target_commerce_type)
                self.model.online_retailer_schedule.remove(self)
            elif self.commerce_type == CommerceType.settled_shop:
                target_commerce_type = choice(CommerceModel.settled_shop_policy)
                ECommerceAgent.transform_commerce_type(self, target_commerce_type)
                self.model.settled_shop_schedule.remove(self)



    @classmethod
    def transform_commerce_type(cls, commerce_agent, target_commerce_type):
        target_commerce_agent = None
        if commerce_agent.commerce_type != target_commerce_type:
            if target_commerce_type == CommerceType.offline_retailer:
                last_id = get_last_agent_id_from_schedule(commerce_agent.model.offline_retailer_schedule)
                unique_id = (int(last_id) + 1) if last_id is not None else 1
                unique_id = 'offline_retailer_' + unique_id
                rental_cost = 100
                target_commerce_agent = OfflineRetailerAgent(unique_id, commerce_agent.model, rental_cost)
                target_commerce_agent.step_profits = commerce_agent.step_profits
                commerce_agent.model.offline_retailer_schedule.add(target_commerce_agent)
            elif target_commerce_type == CommerceType.online_retailer:
                last_id = get_last_agent_id_from_schedule(commerce_agent.model.online_retailer_schedule)
                unique_id = (int(last_id) + 1) if last_id is not None else 1
                unique_id = 'online_retailer_' + unique_id
                technical_cost = 100
                target_commerce_agent = OnlineRetailerAgent(unique_id, commerce_agent.model, technical_cost)
                target_commerce_agent.step_profits = commerce_agent.step_profits
                commerce_agent.model.online_retailer_schedule.add(target_commerce_agent)
            elif target_commerce_type == CommerceType.settled_shop:
                last_id = get_last_agent_id_from_schedule(commerce_agent.model.settled_shop_schedule)
                unique_id = (int(last_id) + 1) if last_id is not None else 1
                unique_id = 'settled_shop_' + unique_id
                rental_cost = 40
                subsidy_cost = 10
                # 随机选取一个平台电商，作为Settled Shop所依赖的电商平台
                platform_e_commerce_agent = choice(commerce_agent.model.platform_e_commerce_schedule.agents)
                target_commerce_agent = SettledShopAgent(unique_id, commerce_agent.model, rental_cost, subsidy_cost, platform_e_commerce_agent)
                target_commerce_agent.step_profits = commerce_agent.step_profits
                commerce_agent.model.settled_shop_schedule.add(target_commerce_agent)
        return target_commerce_agent

    def __is_exit_by_profit(self):
        """判断是否连续三年亏损，如果亏损，退出。"""
        step_len = len(self.step_profits)
        if step_len >=3:
            if self.step_profits[step_len-1] <= 0 and self.step_profits[step_len-2] <= 0 and self.step_profits[step_len-3] <= 0:
                return True
        return False

    def drop_out(self):
        self.is_active=False


class OfflineRetailerAgent(ECommerceAgent):
    """
    The Offline Retailer Agent, as the child class of ECommerce Agent.
    """

    def __init__(self, unique_id, model, rental_cost):
        super().__init__(unique_id, model, CommerceType.offline_retailer, rental_cost, 0, 0, [])


class OnlineRetailerAgent(ECommerceAgent):
    """
    The Online REtailer Agent, as the child class of ECommerce Agent.
    """

    def __init__(self, unique_id, model, technical_cost):
        super().__init__(unique_id, model, CommerceType.online_retailer, 0, technical_cost, 0, [])


class PlatformECommerceAgent(ECommerceAgent):
    """
    The Platform E-Commerce Agent such as Jingdong, as the child class of ECommerce Agent.
    """

    def __init__(self, unique_id, model, technical_cost, subsidy_cost):
        super().__init__(unique_id, model, CommerceType.platform_commerce, 0, technical_cost, subsidy_cost, [])


class SettledShopAgent(ECommerceAgent):
    """
    The Settled Shop Agent, which is settled in the E-Commerce Platform Agent,
    as the child class of ECommerce Agent.
    """
    platform_agent = None

    def __init__(self, unique_id, model, rental_cost, subsidy_cost, platform_e_commerce_agent=None):
        super().__init__(unique_id, model, CommerceType.settled_shop, rental_cost, 0, subsidy_cost, [])
        self.platform_agent = platform_e_commerce_agent
