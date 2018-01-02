name := "nuclio-test-handler"
organization := "io.nuclio"
version := "1.0-SNAPSHOT"
description := "Nuclio Test Java Handler"
crossPaths := false
autoScalaLibrary := false

libraryDependencies += "io.nuclio" % "nuclio-sdk" % "1.0-SNAPSHOT" from "file://" + baseDirectory.value + "/nuclio-sdk-1.0-SNAPSHOT.jar"
