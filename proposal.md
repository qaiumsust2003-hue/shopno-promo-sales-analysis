# Proposal: Which Promotions Lift Supermarket Sales?

## 1. Research question
For a supermarket chain such as Shopno (Shwapno) Superstore, **how much does weekly store sales increase with each type of promotional activity (in-store display placement, mailer features, and price discounts including coupons)?**

Technique: regression (multiple linear regression as the baseline, then a random forest regressor to check for non-linear effects), as covered in class.

- **Target:** `sales_value`, total sales per store per week (modelled on the log scale).
- **Predictors:** `share_on_display`, `share_in_mailer`, `discount_rate`, `coupon_rate`, with `n_lines` (a traffic/size proxy) and store identity used as controls.
- **Evaluation:** train/test split (75/25), R² and RMSE on held-out weeks, plus coefficient interpretation for the linear model.

A quick check on the processed table shows the signal is there: a linear model on the four promotion variables alone reaches a test R² of about 0.45 (log sales), rising to about 0.77 once store size is controlled for. Much of that gain is store size, so the proposal treats store size as a confounder (larger stores promote more items), not as a promotion effect.

## 2. Dataset
- **Name:** Complete Journey retail shopping data (84.51°), packaged as the R package `completejourney`
- **Link:** https://github.com/bradleyboehmke/completejourney (original files: https://www.8451.com/area51)
- **License:** CC0
- **Content:** 2,469 households over 2017; 1.47M transaction lines; product-store-week display and mailer placements (20.9M rows).
- **Processed table:** `data/processed/weekly_store_sales.csv`, 7,341 store-week rows built by `data/prepare_data.py`.
- **Why a stand-in:** Shopno does not publish transaction data. This dataset has the same structure, so the method carries over, but results describe this dataset only, not Shopno.

## 3. Scan of existing work
**Source 1.** Blattberg, R. C., Briesch, R., & Fox, E. J. (1995). "How Promotions Work." *Marketing Science*, 14(3), G122-G132. A review of what the promotion literature had established by the mid-1990s about promotional price cuts and their effect on sales. It frames the central issue for this project: a sales jump during a promotion is not the same as an incremental gain, because some of it comes from shoppers shifting purchases in time. Record: https://www.kellogg.northwestern.edu/faculty/research/detail/1995/how-promotions-work

**Source 2.** van Heerde, H. J., Leeflang, P. S. H., & Wittink, D. R. (2000). "The Estimation of Pre- and Postpromotion Dips with Store-Level Scanner Data." *Journal of Marketing Research*, 37(3), 383-395. Uses store-level scanner data, the same unit of analysis as this project, to estimate how sales dip before and after a promotion. Record: https://econpapers.repec.org/RePEc:gro:rugsom:99b36 (working-paper version)

**Gap this project addresses (my own framing, not a claim from the sources).** Both works study promotions on price. This project compares price discounts against non-price tools (display and mailer exposure) in one model, on a public dataset, and is deliberately simpler than the cited work: it does not model pre/post-promotion dips.

## 4. Limitations
- Public stand-in data, not Shopno.
- Observational data: promotion shares are correlated with store size, so effects are associations, not causal estimates. Store fixed effects will be used to reduce this.
- Weekly aggregation hides within-week timing and the pre/post dips described in Source 2.

## 5. Plan
1. Exploratory analysis and cleaning of `weekly_store_sales.csv`.
2. Baseline linear regression with store controls.
3. Random forest regressor and feature importance for comparison.
4. Report promotion effects and held-out accuracy.
