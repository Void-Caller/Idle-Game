
class Upgrade:
    """
    /param max_level - max level of upgrade
    /param upgrade_cost array of (Decimal) upgrade cost, 
        must cotain {max_level} elements or 1 element.
        if contains {max_level} cost_incr_mult and cost_incr_static should be None
            eg for max_level=3 : upgrade_cost = [1, 10, 20];
    /param (optional) cost_incr_mult Decimal
        multiplier for cost increase
            if level 1 cost 10 and cost_incr_mult=1.5 then
                level 2 will cost 15
                level 3 will cost 22,5
                etc
    /param (optional) cost_incr_static Decimal
        static value for cost increase
            if level 1 cost 10 and cost_incr_static=10 then
                level 2 will cost 20
                level 3 will cost 30
                etc
         
    """
    
    def __init__(self, max_level, currency_cost_type, upgrade_cost=None, cost_incr_mult=None, cost_incr_static=None):
        self.current_level = 0
        self.max_level = max_level
        
        if not (len(upgrade_cost)==1 or len(upgrade_cost)==max_level)
            raise Exception("upgrade_cost must contain 1 or max_level elements.")
            
        self.upgrade_cost = upgrade_cost
        self.cost_incr_mult = cost_incr_mult
        self.cost_incr_static = cost_incr_static
        self.currency_cost_type = currency_cost_type
        
        self.next_level_cost = upgrade_cost[0]
    
    def upgrade(self):
        # TODO currency remove
        
        cost = self.get_upgrade_cost()
        
        # TODO
        # if user.currency < cost
        #   raise Exception / return ?
        
        if self.current_level == self.max_level:
            return;
        #   raise Exception / return ?
            
        self.current_level = self.current_level + 1
        self.next_level_cost = upgrade_cost[self.current_level]
        
        
    def get_upgrade_cost(self):
        
        upgrade_cost = self.next_level_cost;
        
        if len(upgrade_cost) > 1:
            return upgrade_cost[self.current_level]
            
        if not self.cost_incr_mult == None:
            upgrade_cost *= self.cost_incr_mult
            
        if not self.cost_incr_static == None:
            upgrade_cost += self.cost_incr_static
        
        return upgrade_cost
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    