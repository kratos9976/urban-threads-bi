# Step 1 — Business Case: Urban Threads

## The Business
**Urban Threads** is a fictional Australian fashion & apparel retailer, selling online
and through 5 physical stores: Melbourne, Sydney, Brisbane, Perth, Adelaide.
Product range: menswear, womenswear, footwear, accessories.

## Business Problem
Leadership suspects revenue growth is stalling in some regions, returns are eating
into margin, and inventory isn't allocated well across stores vs. online. They want
a BI platform that gives fast, trustworthy answers instead of waiting days for
someone to build a spreadsheet.

## Stakeholders
| Stakeholder | Concern |
|---|---|
| CEO | Overall revenue & growth trajectory |
| Head of Retail Operations | Store-level performance, staffing vs. sales |
| Marketing Director | Campaign/discount effectiveness, customer segments |
| Supply Chain Manager | Inventory turnover, stockouts, overstock |
| Customer Experience Lead | Return rates, reasons, satisfaction |

## Objectives
1. Understand revenue trends by region, channel (online vs. store), and product category
2. Identify what's driving product returns and reduce the return rate
3. Improve inventory allocation to cut stockouts and overstock
4. Segment customers to inform marketing spend
5. Let non-technical stakeholders ask questions in plain English (Step 7 AI layer)

## Key KPIs
- Revenue (total, by region, by channel, by category)
- Average Order Value (AOV)
- Return rate (%) and return reasons
- Inventory turnover ratio
- Stockout frequency
- Customer retention / repeat purchase rate
- Discount effectiveness (uplift vs. margin erosion)

## Requirements
- **Data**: customers, products, orders, stores, inventory, returns, discounts (Step 2)
- **Database**: normalized PostgreSQL schema, queryable for all KPIs above (Step 3)
- **Analysis**: cleaned, EDA-ready dataset surfacing key patterns (Step 4)
- **Dashboards**: Executive, Sales, Customer, Inventory views (Step 5)
- **API**: endpoints serving KPIs and raw analytics (Step 6)
- **AI layer**: natural-language Q&A over the data + auto-generated insights (Step 7)

## Scope Notes
This is a portfolio prototype, not a production system — data is synthetic,
infra is free-tier/local, and the goal is to demonstrate the full BI lifecycle
end-to-end rather than handle real production scale.
