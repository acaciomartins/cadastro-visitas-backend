from rest_framework import serializers
from .models import Visita, Loja, Rito, Grau, Potencia

class LojaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loja
        fields = ['id', 'nome']

class RitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rito
        fields = ['id', 'nome']

class GrauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grau
        fields = ['id', 'numero', 'nome']

class PotenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Potencia
        fields = ['id', 'nome']

class VisitaSerializer(serializers.ModelSerializer):
    loja = LojaSerializer()
    rito = RitoSerializer()
    grau = GrauSerializer()
    potencia = PotenciaSerializer()

    class Meta:
        model = Visita
        fields = ['id', 'loja', 'data', 'rito', 'grau', 'potencia', 'created_at', 'updated_at']

    def create(self, validated_data):
        loja_data = validated_data.pop('loja')
        rito_data = validated_data.pop('rito')
        grau_data = validated_data.pop('grau')
        potencia_data = validated_data.pop('potencia')

        loja = Loja.objects.get_or_create(**loja_data)[0]
        rito = Rito.objects.get_or_create(**rito_data)[0]
        grau = Grau.objects.get_or_create(**grau_data)[0]
        potencia = Potencia.objects.get_or_create(**potencia_data)[0]

        visita = Visita.objects.create(
            loja=loja,
            rito=rito,
            grau=grau,
            potencia=potencia,
            **validated_data
        )
        return visita

    def update(self, instance, validated_data):
        loja_data = validated_data.pop('loja', None)
        rito_data = validated_data.pop('rito', None)
        grau_data = validated_data.pop('grau', None)
        potencia_data = validated_data.pop('potencia', None)

        if loja_data:
            loja = Loja.objects.get_or_create(**loja_data)[0]
            instance.loja = loja
        if rito_data:
            rito = Rito.objects.get_or_create(**rito_data)[0]
            instance.rito = rito
        if grau_data:
            grau = Grau.objects.get_or_create(**grau_data)[0]
            instance.grau = grau
        if potencia_data:
            potencia = Potencia.objects.get_or_create(**potencia_data)[0]
            instance.potencia = potencia

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance 