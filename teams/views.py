from django.shortcuts import render
from rest_framework.views import APIView, Response, Request
from django.forms.models import model_to_dict
from datetime import datetime
from teams.models import Team


class TeamView(APIView):
    def get(self, request: Request) -> Response:
        teams = Team.objects.all()

        team_list = [model_to_dict(team) for team in teams]

        return Response(team_list, 200)

    def post(self, request: Request) -> Response:
        team = Team.objects.create(**request.data)
        team_dict = model_to_dict(team)

        if team_dict["titles"] < 0:
            return Response({"error": "titles cannot be negative"}, 400)

        f_c_year = 1930
        valid_years = []
        actual_year = datetime.now().year

        while f_c_year <= actual_year:
            valid_years.append(f_c_year)
            f_c_year
            f_c_year += 4

        date_str = team_dict["first_cup"]
        date_f = datetime.strptime(date_str, "%Y-%m-%d")

        if valid_years.count(date_f.year) == 0:
            return Response({"error": "there was no world cup this year"}, 400)

        possible_titles = 0
        t_f_cup = date_f.year

        while t_f_cup <= actual_year:
            t_f_cup += 4
            possible_titles += 1

        if team_dict["titles"] > possible_titles:
            return Response(
                {"error": "impossible to have more titles than disputed cups"}, 400
            )

        return Response(team_dict, 201)


class TeamDetailView(APIView):
    def get(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        team_dict = model_to_dict(team)
        return Response(team_dict, 200)

    def patch(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        for key, value in request.data.items():
            setattr(team, key, value)

        team.save()

        team_dict = model_to_dict(team)

        return Response(team_dict, 200)

    def delete(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        team.delete()

        return Response(status=204)
