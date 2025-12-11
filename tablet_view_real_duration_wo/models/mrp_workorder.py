# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    # Flag untuk track apakah user sedang bekerja (tidak di-pause manual)
    is_user_working = fields.Boolean(
        string='Is User Working',
        default=False,
        help='Flag to indicate if user is actively working, prevents auto-pause on tablet view close'
    )

    @api.depends('time_ids.duration', 'time_ids.date_start', 'time_ids.date_end')
    def _compute_duration(self):
        """
        Override compute duration untuk include real-time calculation
        dari timer yang masih berjalan meskipun tablet view ditutup.
        """
        for order in self:
            # Hitung durasi dari timer yang sudah selesai (date_end != False)
            completed_duration = sum(order.time_ids.filtered(lambda t: t.date_end).mapped('duration'))
            
            # Hitung durasi dari timer yang masih berjalan (date_end == False)
            running_timers = order.time_ids.filtered(lambda t: not t.date_end and t.date_start)
            running_duration = 0.0
            
            for timer in running_timers:
                # Hitung durasi dari date_start sampai sekarang
                time_diff = datetime.now() - timer.date_start.replace(microsecond=0)
                # Konversi ke menit (float)
                running_duration += time_diff.total_seconds() / 60.0
            
            order.duration = completed_duration + running_duration

    def get_working_duration(self):
        """
        Method untuk dipanggil dari JavaScript widget untuk update timer secara real-time.
        Method ini akan return durasi total termasuk yang sedang berjalan.
        """
        self.ensure_one()
        running_duration = 0.0
        running_timers = self.time_ids.filtered(lambda t: not t.date_end and t.date_start)
        
        for timer in running_timers:
            time_diff = datetime.now() - timer.date_start.replace(microsecond=0)
            running_duration += time_diff.total_seconds() / 60.0
        
        return running_duration

    def button_start(self):
        """Override button_start to set is_user_working flag"""
        res = super(MrpWorkorder, self).button_start()
        self.write({'is_user_working': True})
        return res

    def button_pending(self):
        """Override button_pending - hanya pause jika user benar-benar klik pause"""
        res = super(MrpWorkorder, self).button_pending()
        self.write({'is_user_working': False})
        return res
    
    def button_finish(self):
        """Override button_finish to set is_user_working flag to False"""
        res = super(MrpWorkorder, self).button_finish()
        self.write({'is_user_working': False})
        return res

    def action_back(self):
        """
        Override action_back (ketika user close tablet view).
        JANGAN auto-pause, biarkan timer tetap berjalan.
        """
        # Cek apakah ada method action_back di parent
        if hasattr(super(MrpWorkorder, self), 'action_back'):
            # Simpan status working sebelum action_back
            working_status = {wo.id: wo.is_user_working for wo in self}
            
            # Panggil parent method
            res = super(MrpWorkorder, self).action_back()
            
            # Restore status working dan cegah auto-pause
            for wo in self:
                if working_status.get(wo.id):
                    # Jika user sedang working, restart timer yang mungkin di-stop oleh action_back
                    running_timers = wo.time_ids.filtered(lambda t: not t.date_end and t.date_start)
                    if not running_timers and wo.state == 'progress':
                        # Jika timer di-stop, restart
                        wo.button_start()
            
            return res
        return {'type': 'ir.actions.act_window_close'}
    
    @api.model
    def _cron_update_real_time_duration(self):
        """
        Cron job untuk force update computed field duration.
        Ini memastikan duration ter-update secara real-time meskipun view tidak dibuka.
        """
        # Ambil semua workorder yang sedang progress dan ada timer yang berjalan
        workorders = self.search([
            ('state', '=', 'progress'),
            ('is_user_working', '=', True)
        ])
        
        # Force recompute
        for wo in workorders:
            wo._compute_duration()

