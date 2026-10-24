# Worked example: customer KRA PIN

Observed 2026-10-13. Recheck before reuse.

- Public article: https://docs.cosmopawa.com/knowledge-base/adding-a-customers-kra-pin-using-ctrl-p/
- Title: **Adding a Customer’s KRA PIN Using Ctrl + P**
- Slug: `adding-a-customers-kra-pin-using-ctrl-p`
- Excerpt: "Add a customer’s name and KRA PIN to a PawaPos sale using Ctrl + P on the payment screen, with the correct verification mode and save steps."
- Category: **Front Office**; checkout entry belongs to Front Office. Confirmed checked in editor and listed at https://docs.cosmopawa.com/article-categories/front-office/.
- WordPress post: 150, Published, `ht_kb` as shown by editor's article-list URL.
- Local article: `D:\cp\pp\pawapos-fo\PawaPosFo\docs\articles\adding-a-customers-kra-pin-using-ctrl-p.md`.
- Saved public-page screenshot: [worked-example-public.jpg](../assets/worked-example-public.jpg); authenticated toolbar excluded by crop.
- Saved category-listing screenshot: [worked-example-category.jpg](../assets/worked-example-category.jpg).

## Evidence ledger

Front Office HEAD `79a0183a42d2ebe015262e1639ff21c68dd9895d`; database-migration HEAD `4cce45b76188d565bf50dba3358d238c1ea09e4e`. Inspected implementation and migration files had no local modifications. The local article Markdown was untracked and is not attributed to that commit. Paths below are relative to those repositories.

| Claim | Evidence and conclusion |
|---|---|
| Ctrl+P opens Customer Details on payment screen | `frm_pay_point.cs:1019-1021` opens `new FiscalCustomer(_receipt).ShowDialog()` for `Keys.Control | Keys.P`; handler first calls `ProcessShortCut`. At `1065-1081`, that helper strips modifiers and can consume P as a configured payment shortcut when focus is outside TextBoxX. This proves the mapping subject to interception, not universal availability. Target shortcut configuration/focus was not tested. |
| Dialog/field names | `dialogs/FiscalCustomer.Designer.cs:108,174,190,219,248`: `Name:`, `Verification Mode:`, `Value:`, `Phone No:`, `Customer Details`. Colons are part of labels. Runtime UI was not inspected. |
| Tax option default | `pawapos-dblog/0_0_0_10.sql:2,4,9` seeds TIN / type 1, makes it default, uppercases descriptions to **TAX IDENTIFICATION NUMBER**. **KRA PIN** is not the seeded dropdown label. |
| Site customization | `dialogs/FiscalCustomer.cs`, `ReceiptChecker_Load`, loads `type_code,description from id_type where active order by type_code` and selects configured default. A read-only connected configuration query returned TIN / 1 / TAX IDENTIFICATION NUMBER / active true / def true. Connector deployment identity was not independently established; do not generalize this to every customer. |
| Name and Value required | `FiscalCustomer.cs`, `btn_save_Click`, rejects empty `txt_kra_pin.Text` and `txt_fiscal_name.Text`. No phone-empty check in that handler. `classes/Receipt.cs:128`, `SetFiscalCustomer`, assigns the object and returns non-null. No tax-authority validation or latency guarantee follows from this setter. |
| Phone can populate fields | `FiscalCustomer.cs`, `txt_phone_Leave`, looks up `cash_customer` by phone and, if found, sets name, value, phone, and type. The lookup code was inspected; no real customer records queried and no runtime lookup tested. |
| Phone downstream behavior | `0_0_0_10.sql:3` makes phone the `cash_customer` primary key. `Receipt.cs:550-552` prepares an INSERT/ON CONFLICT(phone) update for fiscal details. Absence of a dialog required-field check does not prove blank-phone use is appropriate end to end; repeated blank values could share a stored key. No persistence execution or blank-phone test was performed. |
| Save control | `FiscalCustomer.Designer.cs:63-74` configures `btn_save` with `Resources.save31` and a click handler, but no `Text = "Save"`. Calling it the **save icon button** is supported; an exact visible **Save** caption is not verified. `btn_save_Click` returns OK after a non-null setter. |
| Reopen/correct before finalization | The same payment handler opens the dialog again; constructor/load retrieves current receipt fiscal details. This supports in-progress correction. It does not establish a post-finalization amendment workflow. |
| Receipt output | Article conditions the check on receipt setup. Printed customer fields, downstream fiscal submission, and transaction persistence were not verified in this run. Do not strengthen this into guaranteed receipt output. |

## Article pattern and review limits

The local Markdown and rendered article agree on purpose, preparation, seven numbered actions, correction before finalizing, and concise troubleshooting. The rendered article has readable heading hierarchy, number ordering, emphasis and a Front Office breadcrumb; the category listing also shows its excerpt.

The existing article calls the save icon a **Save** button and asks users to have a phone number ready. Future revisions should distinguish an icon's action from an exact visible caption and recommended preparation from a mandatory field. Its Ctrl+P troubleshooting should account for configured payment-shortcut interception, after target configuration is checked. Do not silently change this live article during skill creation.

The claim that TIN is used for a KRA PIN is the task's domain context; the inspected setter stores the supplied identifier without verifying it with KRA. This is an entry guide, not a tax verification guarantee. A running POS test with non-customer data, known product version, and target configuration is still needed to verify runtime labels, blank-phone behavior and receipt output. The browser confirmed publication and category placement in the existing authenticated session; an independent anonymous session was not available, although the toolbar reported the article unrestricted.
