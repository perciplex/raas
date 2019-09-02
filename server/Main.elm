import Browser
import Html exposing (Html, text, pre, div, span)
import Html.Attributes exposing (style)
import Json.Decode as Decode
import Http
import Debug


type alias Job =
  { id : String
  , gitUrl : String
  , status : Status
  }

type alias Result = String

type Status 
  = Queued
  | Running String
  | Complete Result


main =
  Browser.element
    { init = init
    , update = update
    , subscriptions = subscriptions
    , view = view
    }

type Model
  = Failure String
  | Loading
  | Success (List Jobs)

init : () -> (Model, Cmd Msg)
init _ =
  ( LoadingFields
  , Http.request
    { method = "GET"
    , url = "/jobs"
    , headers = []
    , body = Http.emptyBody
    , timeout = Nothing
    , tracker = Nothing
    , expect = Http.expectJson GotJobs jobDecoder
    }
  )

  
type Msg
  = GotJobs (Result Http.Error (List Jobs))