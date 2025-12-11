# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class MrpWorkcenterProductivity(models.Model):
    _inherit = 'mrp.workcenter.productivity'

    @api.depends('date_end', 'date_start')
    def _compute_duration(self):
        """
        Override compute duration untuk include real-time calculation
        ketika timer masih berjalan (date_end == False)
        """
        for blocktime in self:
            if blocktime.date_start and blocktime.date_end:
                # Timer sudah selesai, hitung normal
                blocktime.duration = blocktime.loss_id._convert_to_duration(
                    blocktime.date_start.replace(microsecond=0),
                    blocktime.date_end.replace(microsecond=0),
                    blocktime.workcenter_id
                )
            elif blocktime.date_start and not blocktime.date_end:
                # Timer masih berjalan, hitung sampai sekarang
                current_time = datetime.now()
                blocktime.duration = blocktime.loss_id._convert_to_duration(
                    blocktime.date_start.replace(microsecond=0),
                    current_time.replace(microsecond=0),
                    blocktime.workcenter_id
                )
            else:
                blocktime.duration = 0.0
