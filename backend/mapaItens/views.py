from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from item.models import Item
from .utils import gerar_coordenadas
import random

class ItensProximosView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # 1) Pegar latitude/longitude do request, ou gerar aleatórias se não vierem
        lat_raw = request.data.get("latitude")
        lon_raw = request.data.get("longitude")

        try:
            if lat_raw is None or lat_raw == "":
                usuario_lat = random.uniform(-90.0, 90.0)
            else:
                usuario_lat = float(lat_raw)
        except (TypeError, ValueError):
            usuario_lat = random.uniform(-90.0, 90.0)

        try:
            if lon_raw is None or lon_raw == "":
                usuario_lon = random.uniform(-180.0, 180.0)
            else:
                usuario_lon = float(lon_raw)
        except (TypeError, ValueError):
            usuario_lon = random.uniform(-180.0, 180.0)

        # 2) Quantidade de itens (default 10)
        try:
            qtd_itens = int(request.data.get("qtd_itens", 20))
        except (TypeError, ValueError):
            qtd_itens = 20

        # 3) Buscar itens do banco
        itens = list(Item.objects.all())
        if not itens:
            return Response([], status=200)

        # 4) Garantir pesos como float 
        for it in itens:
            try:
                it._peso_float = float(it.peso) if it.peso is not None else 1.0
            except (TypeError, ValueError):
                it._peso_float = 1.0

        pesos = [it._peso_float for it in itens]

        # 5) Gerar resposta — aqui usamos coordenadas do item se existem,
        #    caso contrário geramos coord próxima (sem sobrescrever banco).
        itens_proximos = []
        for _ in range(qtd_itens):
            escolhido = random.choices(itens, weights=pesos, k=1)[0]

            if escolhido.latitude is None or escolhido.longitude is None:
                lat, lon = gerar_coordenadas(usuario_lat, usuario_lon)
            else:
                lat, lon = gerar_coordenadas(usuario_lat, usuario_lon)

            itens_proximos.append({
                "id": escolhido.id,
                "nome": escolhido.nome,
                "tipo": escolhido.tipo,
                "latitude": lat,
                "longitude": lon,
                "peso": escolhido._peso_float,
                "imagem": str(escolhido.imagem) if escolhido.imagem else None,
            })

        return Response(itens_proximos)
