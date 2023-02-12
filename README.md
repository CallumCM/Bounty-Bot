# Bounty Bot
Replit's new Bounties feature is great! But I want to stay on top of the latest bounties, without perpetually keeping a tab open. The solution? Write a Discord bot to notify me when there's a new bounty.

# How it Works
Every 5 minutes the bot will use Selenium to send a request from [replit.com/bounties](https://replit.com/bounties) to [replit.com/graphql](https://replit.com/graphql) asking it for the most recent bounties. It then uses a JSON cache of the previous few bounties in order to calculate which bounties are new, and it sends a Discord embed showing details about the new bounties in the first channel in your server with the name `replit-bounties` or `bounties`.
