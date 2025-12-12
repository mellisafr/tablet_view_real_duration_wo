# Tablet View Real Duration for Work Order - Odoo 16

## Description
Odoo 16 module to keep work order real duration running in real-time even when tablet view is closed. Timer will continue running in background until user clicks Pause/Done button.

## Features
- ✅ Real-time duration calculation continues even when tablet view is closed
- ✅ Duration auto-updates with computed field mechanism
- ✅ Timer only stops when user manually clicks Pause or Done button
- ✅ `is_user_working` status tracking to prevent auto-pause
- ✅ Override compute duration for `mrp.workorder` and `mrp.workcenter.productivity`
- ✅ Uses `@api.depends` for more accurate auto-updates

## Problem Solved
In standard Odoo, when an operator opens tablet view to start a work order, then closes the tablet view to check something else, the timer automatically pauses. This module solves that issue by keeping the timer running until the operator actually clicks the Pause button.

## Installation
1. Clone or download this module to your Odoo custom addons directory:
   ```bash
   cd /path/to/your/odoo/custom_addons
   git clone https://github.com/mellisafr/odoo16-tablet_view_real_time_wo.git tablet_view_real_duration_wo
   ```

2. Restart Odoo server:
   ```bash
   sudo systemctl restart odoo
   # or
   ./odoo-bin restart
   ```

3. Update Apps List:
   - Go to Odoo → Apps → Update Apps List

4. Install module:
   - Search for "MRP Workorder Real-Time Duration"
   - Click Install

## Configuration
No special configuration required. Module will work immediately after installation.

**Auto-Update Mechanism:**
This module uses computed fields with `@api.depends` that automatically trigger whenever the field is accessed, ensuring duration is always accurate without needing cron jobs.

## Usage
1. Go to Manufacturing → Operations
2. Select the work order you want to work on
3. Click **Open Tablet View** button
4. Click **Start** button to start the timer
5. **Close tablet view** to check other things → Timer keeps running! ✅
6. Reopen work order → Duration will continue to increase in real-time
7. Click **Pause** button to pause timer (if needed)
8. Click **Done** button to finish work order

**`Real Duration` field** will display real-time duration including currently running timer.

## Technical Details
### Models Modified:
- `mrp.workorder` - Override `_compute_duration()` for real-time calculation
- `mrp.workcenter.productivity` - Override `_compute_duration()` for running timers

### New Fields:
- `is_user_working` (Boolean) - Flag to track working status

### Methods Override:
- `button_start()` - Set `is_user_working = True`
- `button_pending()` - Set `is_user_working = False` (manual pause)
- `button_finish()` - Set `is_user_working = False`
- `action_back()` - Prevent auto-pause on tablet view close
- `_compute_duration()` - Real-time calculation with `datetime.now()`

## Dependencies
- `mrp` (Manufacturing)
- `mrp_workorder` (Work Order Management)

## Version
- **Odoo Version:** 16.0
- **Module Version:** 1.0
- **License:** OPL-1

## Author
**Mellisa FR**
- Find me at: https://www.linkedin.com/in/mellisafr/

## Support
If you have any issues or questions, please create an issue in this repository.
