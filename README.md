## Disclaimer

First of all, a warning: if you’ve never used gst-launch before (or gstreamer for that matter), you probably won’t find this tool very easy to use.

On the other hand, if you want to reconfigure and play with your gstreamer pipelines via the command line while they’re running, this is the tool for you.

## Running without installation

```
python -m gstlaunchdynamic
```

## Installation

### Local

```
pip install -e .
```

### Remote

```
pip install -e git+https://github.com/albfan/gst-launch-repl
```

## Usage

```
$ gst-launch-dynamic videotestsrc ! autovideosink
videotestsrc0.pattern=18
```

```
$ gst-launch-dynamic videotestsrc
+autovideosink
videotestsrc0.src->autovideosink0.sink
play
```

## Commands

In all the examples below, {{{<element>}}} refers to the name of the element.  If you haven’t given it a name explicitly, gstreamer assigns names by appending a number to the element type (e.g., videotestsrc0).

### Pipeline state

```
play
pause
stop
```

### Set properties

```
<element>.<property> = <value>
```

### Link elements ==

```
<element>.<pad> -> <element>.<pad>
```

You can omit one or both pad names.

### Unlink elements ==

```
<element>.<pad> x> <element>.<pad>
```

### Add element ==

```
+ type [key=value ...]
```

Same syntax as gst-launch, with a plus sign at the front.

### Remove element ==

```
- <element>
```

### Show pipeline elements

```
pipeline
```

### Help

```
help
```
