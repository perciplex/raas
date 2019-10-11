import Browser
import Html exposing (Html, text, pre, div, span, ul, li)
import Html.Attributes exposing (style, class, classList)
import Json.Decode as Decode
import Http
import Debug


type alias Job =
  { id : String
  , gitUrl : String
  , status : Status
  }

type alias Results = String

type Status 
  = Queued
  | Running String
  | Complete Results

statusDecoder : Decode.Decoder Status
statusDecoder =
    Decode.string
        |> Decode.andThen (\str ->
           case str of
                "QUEUED" ->
                    Decode.succeed Queued
                "RUNNING" ->
                    Decode.succeed (Running "Dev1")
                "COMPLETE" ->
                    Decode.succeed (Complete "Test results")
                somethingElse ->
                    Decode.fail <| "Unknown status: " ++ somethingElse
        )

jobDecoder : Decode.Decoder Job
jobDecoder =
  Decode.map3 Job
    (Decode.at [ "id" ] Decode.string)
    (Decode.at [ "gitUrl" ] Decode.string)
    (Decode.at [ "status" ] statusDecoder)

jobListDecoder : Decode.Decoder (List Job)
jobListDecoder =  (Decode.at [] (Decode.list jobDecoder))


subscriptions : Model -> Sub Msg
subscriptions model =
  Sub.none

main =
  Browser.element
    { init = init
    , update = update
    , subscriptions = subscriptions
    , view = view
    }

type Model
  = Failure String
  | LoadingJobs
  | Jobs (List Job)

init : () -> (Model, Cmd Msg)
init _ =
  ( LoadingJobs
  , Http.request
    { method = "GET"
    , url = "/job"
    , headers = []
    , body = Http.emptyBody
    , timeout = Nothing
    , tracker = Nothing
    , expect = Http.expectJson GotJobs jobListDecoder
    }
  )

  
type Msg
  = GotJobs (Result Http.Error (List Job))


update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    GotJobs (Ok jobs) -> ((Jobs jobs), Cmd.none)
    GotJobs (Err err) -> ((Failure (Debug.toString err)) , Cmd.none)


view : Model -> Html Msg
view model =
  case model of
    Failure msg ->
      text ("I was unable to load the jobs. " ++ msg)

    LoadingJobs ->
      text "LoadingJobs Jobs..."

    Jobs jobs -> (formatJobs jobs)

formatJobs : List Job -> Html Msg
formatJobs jobs = ul [class "list-group"] (List.map formatJob jobs)

formatJob : Job -> Html Msg
formatJob job = li [class "list-group-item d-flex justify-content-between align-items-center"] 
    [ span [class "float-left"] [text job.gitUrl]
    , formatStatus job.status
    ]

formatStatus : Status -> Html Msg
formatStatus status =
    case status of
        Queued -> span [class "float-right badge badge-primary"] [text "QUEUED"]
        Running _ -> span [class "float-right badge badge-primary"] [text "QUEUED"]
        Complete _ -> span [class "float-right badge badge-primary"] [text "QUEUED"]