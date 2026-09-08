from django import forms

from .models import Reservation


class ReservationForm(forms.ModelForm):
    selected_slot = forms.ChoiceField(
        label="Parking slot",
        required=True,
        widget=forms.Select(attrs={"class": "form-select", "id": "id_selected_slot"}),
    )
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"})
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"})
    )

    class Meta:
        model = Reservation
        fields = ["vehicle_type", "vehicle_number", "start_time", "end_time"]
        widgets = {
            "vehicle_type": forms.Select(attrs={"class": "form-select", "id": "id_vehicle_type"}),
            "vehicle_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. GA 2 PA 1234"}),
        }

    def __init__(self, *args, lot=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.lot = lot
        if lot is not None:
            available_slots = lot.slots.filter(status="available").order_by("floor", "slot_number")
            self.fields["selected_slot"].choices = [
                (slot.slot_number, slot.slot_number)
                for slot in available_slots
            ]

    def clean(self):
        cleaned = super().clean()
        start, end = cleaned.get("start_time"), cleaned.get("end_time")
        if start and end:
            if end <= start:
                raise forms.ValidationError("End time must be after start time.")

        selected_slot_number = cleaned.get("selected_slot")
        if self.lot and selected_slot_number:
            selected_slot = self.lot.slots.filter(
                slot_number=selected_slot_number,
                status="available",
            ).first()
            if selected_slot is None:
                self.add_error("selected_slot", "That parking slot is no longer available.")
        return cleaned
