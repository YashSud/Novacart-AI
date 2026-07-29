"""
Synthetic Business Dataset for NovaCart Enterprise AI Assistant.
Contains 16 records across 4 document types: order, refund, support_ticket, warehouse_log.
Includes required edge cases:
- 1 Duplicate record (wh_01 & wh_01_dup)
- 1 Missing field record (sup_04 missing resolution_time)
- 1 Outdated refund policy record (ref_03 referencing deprecated Policy v1.0)
"""

SYNTHETIC_DOCS = [
    # --- ORDERS ---
    {
        "id": "ord_101",
        "doc_type": "order",
        "title": "Order #101 - Smart TV",
        "content": "Order #101 placed on 2026-03-01 for NovaCart Smart TV 55 inch. Status: Delivered.",
        "date": "2026-03-01",
        "customer_id": "cust_881",
        "product_id": "prod_tv",
        "amount": 599.99
    },
    {
        "id": "ord_102",
        "doc_type": "order",
        "title": "Order #102 - Wireless Earbuds Batch",
        "content": "Order #102 placed on 2026-03-03 for NovaCart Earbuds Pro (Batch #WH-MARCH). Status: Returned.",
        "date": "2026-03-03",
        "customer_id": "cust_412",
        "product_id": "prod_earbuds",
        "amount": 89.99
    },
    {
        "id": "ord_103",
        "doc_type": "order",
        "title": "Order #103 - Thermal Receipt Printer",
        "content": "Order #103 placed on 2026-03-05 for Thermal Receipt Printer X2. Status: Returned.",
        "date": "2026-03-05",
        "customer_id": "cust_903",
        "product_id": "prod_printer",
        "amount": 149.50
    },
    {
        "id": "ord_104",
        "doc_type": "order",
        "title": "Order #104 - POS Terminal X1",
        "content": "Order #104 placed on 2026-03-10 for POS Terminal X1 Enterprise. Status: Returned.",
        "date": "2026-03-10",
        "customer_id": "cust_330",
        "product_id": "prod_pos_x1",
        "amount": 299.00
    },

    # --- REFUNDS ---
    {
        "id": "ref_01",
        "doc_type": "refund",
        "title": "Refund #REF-MAR-01 - Defective Earbuds Batch",
        "content": "Refund of $89.99 processed on 2026-03-08 for Order #102. Reason: Water damage caused by defective seals from Warehouse Batch #WH-MARCH. Governed by Refund Policy v2.0.",
        "date": "2026-03-08",
        "order_id": "ord_102",
        "policy_version": "v2.0",
        "status": "approved",
        "amount": 89.99
    },
    {
        "id": "ref_02",
        "doc_type": "refund",
        "title": "Refund #REF-MAR-02 - Cracked Screen POS Terminal",
        "content": "Refund of $299.00 processed on 2026-03-12 for Order #104. Reason: POS Terminal screen cracked during warehouse transport. Governed by Refund Policy v2.0.",
        "date": "2026-03-12",
        "order_id": "ord_104",
        "policy_version": "v2.0",
        "status": "approved",
        "amount": 299.00
    },
    {
        "id": "ref_03",
        "doc_type": "refund",
        "title": "Refund #REF-MAR-03 - Outdated Policy Legacy Refund",
        "content": "Refund of $149.50 processed on 2026-03-15 for Order #103. Reason: Customer changed mind after 45 days. Processed under Policy v1.0 (Deprecated - 60 day window).",
        "date": "2026-03-15",
        "order_id": "ord_103",
        "policy_version": "v1.0 (Deprecated)",  # EDGE CASE: Outdated policy
        "status": "approved_legacy",
        "amount": 149.50
    },
    {
        "id": "ref_04",
        "doc_type": "refund",
        "title": "Refund Policy Summary v2.0",
        "content": "Official NovaCart Refund Policy v2.0 (Effective 2026-01-01): Returns accepted within 30 days. Defective warehouse items receive 100% full refund.",
        "date": "2026-01-01",
        "order_id": "N/A",
        "policy_version": "v2.0",
        "status": "active_policy",
        "amount": 0.0
    },

    # --- SUPPORT TICKETS ---
    {
        "id": "sup_01",
        "doc_type": "support_ticket",
        "title": "Ticket #T-901 - Earbuds Water Ingress Spike",
        "content": "Customer reported Earbuds Pro stopped working after light rain. 45 similar tickets received in March regarding Warehouse Batch #WH-MARCH packaging failure.",
        "date": "2026-03-04",
        "order_id": "ord_102",
        "issue_category": "quality_control",
        "resolution_time": "24h"
    },
    {
        "id": "sup_02",
        "doc_type": "support_ticket",
        "title": "Ticket #T-902 - POS Terminal Transit Damage",
        "content": "Merchant reported POS Terminal X1 box crushed upon delivery. High volume of transit damage reports in March due to new warehouse shipping vendor.",
        "date": "2026-03-11",
        "order_id": "ord_104",
        "issue_category": "logistics_damage",
        "resolution_time": "12h"
    },
    {
        "id": "sup_03",
        "doc_type": "support_ticket",
        "title": "Ticket #T-903 - Late Delivery Complaints",
        "content": "Multiple customers complaining about 4-day delivery delays from Warehouse North in March.",
        "date": "2026-03-14",
        "order_id": "ord_103",
        "issue_category": "delivery_delay",
        "resolution_time": "48h"
    },
    {
        "id": "sup_04",
        "doc_type": "support_ticket",
        "title": "Ticket #T-904 - Missing Accessories Query",
        "content": "Customer inquired about missing power cable in box. Pending customer response.",
        "date": "2026-03-16",
        "order_id": "ord_101",
        "issue_category": "missing_item",
        "resolution_time": None  # EDGE CASE: Missing field
    },

    # --- WAREHOUSE LOGS ---
    {
        "id": "wh_01",
        "doc_type": "warehouse_log",
        "title": "Warehouse Incident Log - Batch WH-MARCH Seal Failure",
        "content": "Warehouse North Incident Log (2026-03-02): Forklift operator damaged humidity seal on Batch #WH-MARCH (Earbuds Pro). Water leakage during storm affected 200 units, leading to high March refunds.",
        "date": "2026-03-02",
        "warehouse_location": "Warehouse North",
        "impact_level": "High"
    },
    {
        "id": "wh_01_dup",
        "doc_type": "warehouse_log",
        "title": "Warehouse Incident Log - Batch WH-MARCH Seal Failure (DUPLICATE)",
        "content": "Warehouse North Incident Log (2026-03-02): Forklift operator damaged humidity seal on Batch #WH-MARCH (Earbuds Pro). Water leakage during storm affected 200 units, leading to high March refunds.",
        "date": "2026-03-02",
        "warehouse_location": "Warehouse North",
        "impact_level": "High"  # EDGE CASE: Duplicate record
    },
    {
        "id": "wh_02",
        "doc_type": "warehouse_log",
        "title": "Warehouse Incident Log - Conveyor Belt Breakdown",
        "content": "Warehouse South Log (2026-03-09): Main conveyor belt jammed for 6 hours. Heavy packages dropped, causing screen damage on POS Terminals.",
        "date": "2026-03-09",
        "warehouse_location": "Warehouse South",
        "impact_level": "Medium"
    },
    {
        "id": "wh_03",
        "doc_type": "warehouse_log",
        "title": "Warehouse Inspection Log - Monthly Audit",
        "content": "Routine monthly inventory audit for March completed with 99.2% stock accuracy across all facilities.",
        "date": "2026-03-20",
        "warehouse_location": "Central Hub",
        "impact_level": "Low"
    }
]
