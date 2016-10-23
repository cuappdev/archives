name          := """podcast-web"""
organization  := "me.archdev"
version       := "1.0.0"
scalaVersion  := "2.11.7"
scalacOptions := Seq("-unchecked", "-feature", "-deprecation", "-encoding", "utf8")

libraryDependencies ++= {
  val akkaStreamV = "2.0-M1"
  val scalaTestV = "3.0.0-M1"
  val scalaMockV = "3.2.2"
  val scalazScalaTestV = "0.2.3"
  val slickVersion = "3.1.0"
  Seq(
    // All of Akka
    "com.typesafe.akka" %% "akka-stream-experimental" % akkaStreamV,
    "com.typesafe.akka" %% "akka-http-core-experimental" % akkaStreamV,
    "com.typesafe.akka" %% "akka-http-spray-json-experimental" % akkaStreamV,
    // Function Relational Model (FRM)
    "com.typesafe.slick" %% "slick" % slickVersion,
    "org.slf4j" % "slf4j-nop" % "1.6.4",
    "joda-time" % "joda-time" % "2.7",
    // Postgres driver
    "org.postgresql" % "postgresql" % "9.4-1201-jdbc41",
    // Bcrypt
    "org.mindrot" % "jbcrypt" % "0.3m",
    // For migrations
    "org.flywaydb" % "flyway-core" % "3.2.1",
    // All testing
    "org.scalatest" %% "scalatest" % scalaTestV % "it,test",
    "org.scalamock" %% "scalamock-scalatest-support" % scalaMockV % "it,test",
    "com.typesafe.akka" %% "akka-http-testkit-experimental" % akkaStreamV % "it,test",
    // FB Graph API Integration
    "com.restfb" % "restfb" % "1.32.0"
  )
}

// Resolving multiple Scala version warning
libraryDependencies ++= Seq(
  "org.scala-lang" % "scala-reflect" % "2.11.7",
  "org.scala-lang.modules" % "scala-xml_2.11" % "1.0.4"
)


lazy val root = project.in(file(".")).configs(IntegrationTest)
  .enablePlugins(JavaAppPackaging, DockerPlugin)


Defaults.itSettings

Revolver.settings


// Docker configs
dockerExposedPorts := Seq(9000)
dockerEntrypoint := Seq("bin/%s" format executableScriptName.value, "-Dconfig.resource=docker.conf")




parallelExecution in Test := false