class Solution:
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        delta = [prices[i+1]-prices[i] for i in range(len(prices)-1)]
        cnt = 0
        for d in delta:
            if d > 0:
                cnt += 1
        return cnt


s = Solution()
print(s.maxProfit([7,1,5,3,6,4]))



