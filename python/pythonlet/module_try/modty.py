#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    NAME
        modtry.py

    DESCRIPTION
        1. linecache
            1) linecache.cache is a {}, key is filename;
            2) linecache index starts from 1 instead of 0, each line has a '\n';
            3) linecache returns empty even if file not existing or lineno not existing;

            # ref: https://blog.csdn.net/Peakulorain/article/details/74944641
            # ref: https://pythoncaff.com/docs/pymotw/linecache-efficient-file-reading/112

        2. udpate a text file via fileinput, or with ... as ..., os.command('sed ...') etc.
            1) file mode:
                r, w, a, b (binary mode), t (text mode)
                t: text mode meaning that \n character will be translated to the host OS line endings
                    when writing to a file
                    and back again when reading.
                x: open for exclusive creation, failing if th efile alrady exists;
                +: open a disk file for updating (reading and writing)

                Many modules opens a file by default with 't' mode as text mode,
                    while gzip.open is binary mode by default.
            2) in Python3, in text mode, read returns Unicode while str in Python2,
               in Python3, in binary mode, read returns a bytes instance.
               <=> use io.open rather than open in Python 2 if forwards compatibility needed.

            3) update file contents on keys or patterns, could do via re + via two with statements;
               update a specific line, could use new variable or via mmap or via fileinput;
               could back up the file, write new content in, rename back
                    or open it with +, read in content, f.seek(0), f.truncate(), write new content back.

                    fileinput: in fileinput.input(...), the original file is moved to a backup file;
                                the standart output is redirected to the original file within the loop;
                                thus any print statements write back into the original file:
                                    print ... = sys.stdout.write(...)
                    mmap: feasible for big file, it could read part of the file into memory;
                        content = mmap.mmap(<filehandle>, <len_to_read>...),
                                content could be updated inplace.

            4) on Linux, sed -i 's/foo/bar/' <filename>

            5) in Python2: print 'a', doesn't add a newline to the output, while print 'a', print('a') do.
                in Python3: print('a', end='')

        3. 3.1) python-natty, similar to com.joestelmach.natty package for Java,
                python-natty itself is written in Java but wrapped for its use in Python using Jpype.
                It depends on Jpype1 and python-dateutil.
                python-dateutil's parse method is used under the hood.

                # ref: https://stackoverflow.com/questions/45810155/
                        segmentation-fault-when-importing-module-in-python
                # ref: https://github.com/eadmundo/python-natty
            3.2) to parse date, time in Java, jython: natty + re + joda.time
                1) com.joestelmach.natty: a natural language parser in Java.
            dir(natty):
                ['ANTLRNoCaseInputStream', 'CalendarSource', 'DateGroup', 'Holiday', 'IcsSearcher', 'NattyTokenSource',
                'ParseListener', 'ParseLocation', 'Parser', 'Season', 'WalkerState', '__name__', 'generated']
            <=> DateGroup, Parser
                parser = natty.Parser()
                dts = parser.parse(start_str).get(0).getDates()
                res = dts.get(0)

            dir(natty.Parser().parse(...).get(0).getDates().get(0)):
                ['UTC', 'after', 'before', 'class', 'clone', 'compareTo', 'date', 'day', 'equals', 'getClass',
                'getDate', 'getDay', 'getHours', 'getMinutes', 'getMonth', 'getSeconds', 'getTime', 'getTimezoneOffset',
                 'getYear', 'hashCode', 'hours', 'minutes', 'month', 'notify', 'notifyAll', 'parse', 'seconds',
                 'setDate', 'setHours', 'setMinutes', 'setMonth', 'setSeconds', 'setTime', 'setYear', 'time',
                 'timezoneOffset', 'toGMTString', 'toLocaleString', 'toString', 'wait', 'year']
            <=> get..., set..., to..

            2) Joda-Time provides a quality replacement for the Java date and time classes.
                Joda-Time is the de facto standard date and time library for Java prior to Java SE 8.
                Users are now asked to migrate to java.time (JSR-310).

            Concepts:
                Immutability 不可变性
                Instant 瞬间性
                Partial 局部性
                Chronology 年表
                Timezone 时区
            Core Classes:
                Instant
                DateTime
                LocalDate
                LocalTime
                LocalDateTime
                Interval 保存了一个开始时刻和一个结束时刻
                Period  保存了一段时间如年月日时分秒等
                Duration    保存了一个精确的毫秒数
                    Period, Duration 可以直接 via self 创建，也可以从 Interval 创建。
                    Joda.time 默认使用 ISO 的日历系统，默认使用 JDK 的时区设置。
                in java v1.7.0_191, org.joda.time.LocalDate was not existing in v1.2.1, but in v2.1.
                        joda.time package: SpecificationVersion: 1.2
                                           ImplementationVersion: 1.2.1.0


            dir(joda.time):
                ['Chronology', 'DateMidnight', 'DateTime', 'DateTimeComparator', 'DateTimeConstants', 'DateTimeField',
                'DateTimeFieldType', 'DateTimeUtils', 'DateTimeZone', 'Duration', 'DurationField', 'DurationFieldType',
                'IllegalFieldValueException', 'Instant', 'Interval', 'JodaTimePermission', 'MutableDateTime',
                'MutableInterval', 'MutablePeriod', 'Partial', 'Period', 'PeriodType', 'ReadWritableDateTime',
                'ReadWritableInstant', 'ReadWritableInterval', 'ReadWritablePeriod', 'ReadableDateTime',
                'ReadableDuration', 'ReadableInstant', 'ReadableInterval', 'ReadablePartial', 'ReadablePeriod',
                'TimeOfDay', 'YearMonthDay', '__name__', 'base', 'chrono', 'convert', 'field', 'format', 'tz']
            <=> DateTime, Instant, Duration, Interval, Period, format
                The package structure of org.joda.time is designed to separate the methods in the public API
                from the private API.
                The public packages are the root package (under org.joda.time) and the format package.
                The private packages are the base, chrono, convert, field and tz packages.
                Most applications should not need to import classes from the private packages.
                # ref: https://www.joda.org/joda-time/userguide.html

             dir(org.joda.time.DateTime):
                ['__init__', 'afterNow', 'beforeNow', 'centuryOfEra', 'chronology', 'class', 'compareTo', 'dayOfMonth',
                'dayOfWeek', 'dayOfYear', 'equalNow', 'equals', 'era', 'get', 'getCenturyOfEra', 'getChronology',
                'getClass', 'getDayOfMonth', 'getDayOfWeek', 'getDayOfYear', 'getEra', 'getHourOfDay', 'getMillis',
                'getMillisOfDay', 'getMillisOfSecond', 'getMinuteOfDay', 'getMinuteOfHour', 'getMonthOfYear',
                'getSecondOfDay', 'getSecondOfMinute', 'getWeekOfWeekyear', 'getWeekyear', 'getYear',
                'getYearOfCentury', 'getYearOfEra', 'getZone', 'hashCode', 'hourOfDay', 'isAfter', 'isAfterNow',
                'isBefore', 'isBeforeNow', 'isEqual', 'isEqualNow', 'isSupported', 'millis', 'millisOfDay',
                'millisOfSecond', 'minus', 'minusDays', 'minusHours', 'minusMillis', 'minusMinutes', 'minusMonths',
                'minusSeconds', 'minusWeeks', 'minusYears', 'minuteOfDay', 'minuteOfHour', 'monthOfYear', 'notify',
                'notifyAll', 'plus', 'plusDays', 'plusHours', 'plusMillis', 'plusMinutes', 'plusMonths', 'plusSeconds',
                 'plusWeeks', 'plusYears', 'property', 'secondOfDay', 'secondOfMinute', 'toCalendar', 'toDate',
                 'toDateMidnight', 'toDateTime', 'toDateTimeISO', 'toGregorianCalendar', 'toInstant',
                 'toMutableDateTime', 'toMutableDateTimeISO', 'toString', 'toTimeOfDay', 'toYearMonthDay', 'wait',
                 'weekOfWeekyear', 'weekyear', 'withChronology', 'withDate', 'withDurationAdded', 'withField',
                 'withFieldAdded', 'withFields', 'withMillis', 'withPeriodAdded', 'withTime', 'withZone',
                 'withZoneRetainFields', 'year', 'yearOfCentury', 'yearOfEra', 'zone']
            <=> get..., isAfter, is..., minus..., plus..., to..., with...
                org.joda.time: DateTime:        2012-12-15T18:23:55.002Z

            dir(org.joda.time.Period):
                ['__init__', 'class', 'days', 'equals', 'fieldDifference', 'fieldTypes', 'get', 'getClass', 'getDays',
                'getFieldType', 'getFieldTypes', 'getHours', 'getMillis', 'getMinutes', 'getMonths', 'getPeriodType',
                'getSeconds', 'getValue', 'getValues', 'getWeeks', 'getYears', 'hashCode', 'hours', 'indexOf',
                'isSupported', 'millis', 'minusDays', 'minusHours', 'minusMillis', 'minusMinutes', 'minusMonths',
                'minusSeconds', 'minusWeeks', 'minusYears', 'minutes', 'months', 'notify', 'notifyAll', 'periodType',
                'plusDays', 'plusHours', 'plusMillis', 'plusMinutes', 'plusMonths', 'plusSeconds', 'plusWeeks',
                'plusYears', 'seconds', 'size', 'toDurationFrom', 'toDurationTo', 'toMutablePeriod', 'toPeriod',
                'toString', 'values', 'wait', 'weeks', 'withDays', 'withField', 'withFieldAdded', 'withFields',
                'withHours', 'withMillis', 'withMinutes', 'withMonths', 'withPeriodType', 'withSeconds', 'withWeeks',
                'withYears', 'years']
            <=> getValues(), get..., minus..., plus...
                org.joda.time: from Period: array('i',[0, 0, 0, 1, 0, 0, 0, 0])  values
                                    PT86400S toDurationFrom, PT86400S toDurationTo,       P1D toDuration,  P1DtoString.
                # ref: https://stackoverflow.com/questions/17940200/
                        how-to-find-the-duration-of-difference-between-two-dates-in-java

             dir(org.joda.time.format):
                ['DateTimeFormat', 'DateTimeFormatter', 'DateTimeFormatterBuilder', 'DateTimeParser',
                'DateTimeParserBucket', 'DateTimePrinter', 'FormatUtils', 'ISODateTimeFormat', 'ISOPeriodFormat',
                'PeriodFormat', 'PeriodFormatter', 'PeriodFormatterBuilder', 'PeriodParser', 'PeriodPrinter',
                '__name__']
            <=> DateTimeFormat, PeriodFormat, ISOPeriodFormat

            dir(org.joda.time.convert):
                ['AbstractConverter', 'Converter', 'ConverterManager', 'DurationConverter', 'InstantConverter',
                'IntervalConverter', 'PartialConverter', 'PeriodConverter', '__name__']
            <=> Converter, ...Converter

            dir(org.joda.time.base):
                ['AbstractDateTime', 'AbstractDuration', 'AbstractInstant', 'AbstractInterval', 'AbstractPartial',
                'AbstractPeriod', 'BaseDateTime', 'BaseDuration', 'BaseInterval', 'BasePartial', 'BasePeriod',
                '__name__']
            <=> Abstract..., BaseDateTime, Base...

            dir(org.joda.time.chrono):
                ['AssembledChronology', 'BaseChronology', 'BuddhistChronology', 'CopticChronology',
                'EthiopicChronology', 'GJChronology', 'GregorianChronology', 'ISOChronology', 'IslamicChronology',
                'JulianChronology', 'LenientChronology', 'LimitChronology', 'StrictChronology', 'ZonedChronology',
                '__name__']
            <=> ...Chronology, BaseChronology, ISOChronology, GregorianChrology

            dir(org.joda.time.field):
                ['AbstractPartialFieldProperty', 'AbstractReadableInstantFieldProperty', 'BaseDateTimeField',
                'BaseDurationField', 'DecoratedDateTimeField', 'DecoratedDurationField', 'DelegatedDateTimeField',
                'DelegatedDurationField', 'DividedDateTimeField', 'FieldUtils', 'ImpreciseDateTimeField',
                'LenientDateTimeField', 'MillisDurationField', 'OffsetDateTimeField', 'PreciseDateTimeField',
                'PreciseDurationDateTimeField', 'PreciseDurationField', 'RemainderDateTimeField', 'ScaledDurationField',
                 'SkipDateTimeField', 'SkipUndoDateTimeField', 'StrictDateTimeField', 'UnsupportedDateTimeField',
                 'UnsupportedDurationField', 'ZeroIsMaxDateTimeField', '__name__']
            <=> ...Field, BaseDateTimeField, MilllisDurationField

            dir(org.joda.time.tz):
                ['CachedDateTimeZone', 'DateTimeZoneBuilder', 'DefaultNameProvider', 'FixedDateTimeZone',
                'NameProvider', 'Provider', 'UTCProvider', 'ZoneInfoCompiler', 'ZoneInfoProvider', '__name__']
            <=> ...Zone, FixedDateTimeZone, Provider

            3) With Java8 (which integrated Joda-Time concepts)
                    # java.time.... only exists since Java 8, having joda-time concept
                    import java.time.temporal.ChronoUnit
                    import java.time.LocalDate

                before Java8, following package exist:
                    import java.util.Date
                    import java.util.Locale
                    import java.util.Calendar
                    import java.text.SimpleDateFormat

                 dir(java.util):
                    ['AbstractCollection', 'AbstractList', 'AbstractMap', 'AbstractQueue', 'AbstractSequentialList',
                    'AbstractSet', 'ArrayDeque', 'ArrayList', 'Arrays', 'BitSet', 'Calendar', 'Collection',
                    'Collections', 'Comparator', 'ConcurrentModificationException', 'Currency', 'Date', 'Deque',
                    'Dictionary', 'DuplicateFormatFlagsException', 'EmptyStackException', 'EnumMap', 'EnumSet',
                    'Enumeration', 'EventListener', 'EventListenerProxy', 'EventObject',
                    'FormatFlagsConversionMismatchException', 'Formattable', 'FormattableFlags', 'Formatter',
                    'FormatterClosedException', 'GregorianCalendar', 'HashMap', 'HashSet', 'Hashtable',
                    'IdentityHashMap', 'IllegalFormatCodePointException', 'IllegalFormatConversionException',
                     'IllegalFormatException', 'IllegalFormatFlagsException', 'IllegalFormatPrecisionException',
                     'IllegalFormatWidthException', 'IllformedLocaleException', 'InputMismatchException',
                     'InvalidPropertiesFormatException', 'Iterator', 'LinkedHashMap', 'LinkedHashSet', 'LinkedList',
                     'List', 'ListIterator', 'ListResourceBundle', 'Locale', 'Map', 'MissingFormatArgumentException',
                     'MissingFormatWidthException', 'MissingResourceException', 'NavigableMap', 'NavigableSet',
                     'NoSuchElementException', 'Objects', 'Observable', 'Observer', 'PriorityQueue', 'Properties',
                     'PropertyPermission', 'PropertyResourceBundle', 'Queue', 'Random', 'RandomAccess',
                     'ResourceBundle', 'Scanner', 'ServiceConfigurationError', 'ServiceLoader', 'Set',
                     'SimpleTimeZone', 'SortedMap', 'SortedSet', 'Stack', 'StringTokenizer', 'TimeZone', 'Timer',
                     'TimerTask', 'TooManyListenersException', 'TreeMap', 'TreeSet', 'UUID',
                     'UnknownFormatConversionException', 'UnknownFormatFlagsException', 'Vector', 'WeakHashMap',
                     '__name__', 'concurrent', 'jar', 'logging', 'prefs', 'regex', 'spi', 'zip']
                    <=> Calendar, Date, Formatter, Gregoriancalendar, Locale, Properties,
                        TimeZone, Timer, TimerTask, concurrent

                 dir(java.util.Date):
                    ['UTC', 'after', 'before', 'clone', 'compareTo', 'date', 'day', 'getDate', 'getDay', 'getHours',
                    'getMinutes', 'getMonth', 'getSeconds', 'getTime', 'getTimezoneOffset', 'getYear', 'hours',
                    'minutes', 'month', 'parse', 'seconds', 'setDate', 'setHours', 'setMinutes', 'setMonth',
                    'setSeconds', 'setTime', 'setYear', 'time', 'timezoneOffset', 'toGMTString', 'toLocaleString',
                    'year']
                <=> get..., set...

                 dir(java.util.Locale):
                    ['CANADA', 'CANADA_FRENCH', 'CHINA', 'CHINESE', 'ENGLISH', 'FRANCE', 'FRENCH', 'GERMAN', 'GERMANY',
                     'ISO3Country', 'ISO3Language', 'ITALIAN', 'ITALY', 'JAPAN', 'JAPANESE', 'KOREA', 'KOREAN', 'PRC',
                     'PRIVATE_USE_EXTENSION', 'ROOT', 'SIMPLIFIED_CHINESE', 'TAIWAN', 'TRADITIONAL_CHINESE', 'UK',
                     'UNICODE_LOCALE_EXTENSION', 'US', 'clone', 'country', 'displayCountry', 'displayLanguage',
                     'displayName', 'displayScript', 'displayVariant', 'extensionKeys', 'forLanguageTag',
                     'getAvailableLocales', 'getCountry', 'getDefault', 'getDisplayCountry', 'getDisplayLanguage',
                     'getDisplayName', 'getDisplayScript', 'getDisplayVariant', 'getExtension', 'getExtensionKeys',
                     'getISO3Country', 'getISO3Language', 'getISOCountries', 'getISOLanguages', 'getLanguage',
                     'getScript', 'getUnicodeLocaleAttributes', 'getUnicodeLocaleKeys', 'getUnicodeLocaleType',
                     'getVariant', 'language', 'script', 'setDefault', 'toLanguageTag', 'unicodeLocaleAttributes',
                     'unicodeLocaleKeys', 'variant']
                <=> getAvailableLocales, get..., setDefault, toLanguageTag,
                    like macros: CCEFGIJK + US 9 countries

                dir(java.text.SimpleDateFormat):
                    ['2DigitYearStart', 'applyLocalizedPattern', 'applyPattern', 'dateFormatSymbols', 'format',
                    'get2DigitYearStart', 'getDateFormatSymbols', 'parse', 'set2DigitYearStart', 'setDateFormatSymbols',
                     'toLocalizedPattern', 'toPattern']
                <=> applyPattern, parse, format, to....

            4) doc to ...
            5) ref: https://persevere.iteye.com/blog/1755237

        4. module jpype 可以用来在 Python 中和 Java 交互。
            jpype 底层使用的是 JNI， JNI 在 Java 中被用来和底层的 C/C++ 代码进行交互
            => jpype 做了两层转换。

            1) usage
                import jpype

                jvm_path = jpype.getDefaultJVMPath()
                jars = ['/full/path/to/a/needed/.jar']
                jvm_cp = '-Djava.class.path={}'.format(':'.join(jars))
                jpype.startJVM(jvm_path, jvm_cp)

                ...
                java.lang.System.out.println(...)
                ...
                if not jpype.isJVMStarted():
                    jpype.startJVM(jvm_path, jvm_cp)
                else:
                    pass
                ...
                # use com.alibaba.fastjson.JSONObject of Java
                JSONObject = jpype.JClass('com.alibaba.fastjson.JSONObject')
                json_obj = JSONObject.parse(json_str)
                print(json_obj.getString(...))
                ...
                # use self-defined .jar package of Java
                Main = jpype('....Main')
                # run the main class
                Main.main([])

                jpype.shutdownJVM()

            2) jpype两个defects：
                1. couldn't startJVM() twice in a program;
                2. 在 Java 中有很多方法依赖于调用的类来查找信息，但在 Python via jpype 中调用会出错。
                如： instead of java.lang.Class.forName(String className)
                        use Class.forName(className, True, ClassLoader.getSystemClassLoader())
                    instead of java.sql.DriverManager.getConnection(...)
                        use: first instantiate a driver object,
                             then call connect(...).

            3) to implement Java interface via jpype.JProxy in python
                e.g.
                in Java:
                    public interface ITestInterface2
                    {
                        int testMethod();
                        String testMethod2();
                    }
                in Python 2 methods:
                    Method 1. via instance
                        class C(object):
                            def testMethod():
                                pass
                            def testMethod2():
                                pass
                        proxy = jpype.JProxy('ITestInterface2', inst=C())

                    Method 2. via dict
                        def _testMethod():
                            pass
                        def _testMethod2():
                            pass
                        d = { 'testMethod': _testMethod'
                              'testMethod2': _testMethod2}
                        proxy = jpype.JProxy('ITestInterface2', dict=d)

            # ref: https://sdk.cn/news/7225

        5. org.json.simple.* package
            5.1 json module in Python, json in java, jython: org.json.simple.* package
            1) json module from Python2.7 can't be used in jython for version:
            2) check version of WebLogic, jython, wlst:
               $java weblogic.version, $java weblogic.version -verbose
                    WebLogic Server 10.3.6.0.181022 REL9 BUNDLE Patch for BUG28764353 Thu Oct 11 01:12:14 PDT 2018
                    WebLogic Server 10.3.6.0  Tue Nov 15 08:52:36 PST 2011 1441050
               $java weblogic.utils.Versions | egrep -i --color 'wlst|ython|java|json|py'
                    ANTLR Java based compiler generator Client 2.7 Mon Jun 11 12:19:48 EDT 2007  ImplVersion: 2.7.7
                    Eclipse Java Development Tools 3.5.3 Fri May 20 04:56:54 EDT 2011  ImplVersion: 3.5.3.0
                    Common Security SAML 2.0 Management JavaBeans 1.0 Fri Aug 19 08:44:53 MDT 2011  ImplVersion: 6.2.0.0
                    Java.net implementation of MimePull.jar taken from Glassfish JAXWS 2.1.5 1.1 Wed Jul 27 16:50:24 MDT 2011  ImplVersion: 1.3
                    Java.net Stax Extensions 1.0 Tue Jun 3 07:12:06 PDT 2008  ImplVersion: 1.2
                    Java.net xml stream buffer 1.0 Fri Oct 22 10:08:31 PDT 2010  ImplVersion: 0.5
                    Javax Enterprise Activation 1.1 Tue Apr 8 09:31:17 PDT 2008  ImplVersion: 1.1
                    Javax Annotation 1.0 Fri Dec 25 09:02:47 PST 2009  ImplVersion: 1.0
                    Javax Interceptor 1.0 Tue Mar 20 15:37:16 MDT 2007  ImplVersion: 1.0
                    Javax Enterprise Beans  3.0 Mon Jun 11 12:21:01 EDT 2007  ImplVersion: 3.0.1
                    Java Data Objects 2.0 Mon Jun 11 12:20:56 EDT 2007  ImplVersion: 2.0.1
                    Java Enterprise Deployment APIs  1.2 Tue Mar 20 15:37:28 MDT 2007  ImplVersion: 1.2
                    Java Enterprise Messaging  1.1 Mon Jun 11 12:21:11 EDT 2007  ImplVersion: 1.1.1
                    Javax Server Pages  Client Capable 1.3 Tue Jun 21 09:59:39 EDT 2011  ImplVersion: 2.1
                    Java Web Services  2.0 Tue Mar 20 15:37:37 MDT 2007  ImplVersion: 2.0
                    Javax Enterprise Mail 1.1 Mon Jul 6 10:41:09 MDT 2009  ImplVersion: 1.4.1
                    Java Enterprise Management APIs  1.0 Tue Mar 20 15:37:49 MDT 2007  ImplVersion: 1.0
                    Java Persistence Client Capable 1.0 Tue Oct 7 12:18:34 PDT 2008  ImplVersion: 1.0.2
                    Java Connector  1.5 Mon Jun 11 12:22:07 EDT 2007  ImplVersion: 1.5.1
                    Java Authorization Contract for Containers 1.0 Wed Feb 6 15:01:03 PST 2008  ImplVersion: 1.1
                    Javax Enterprise Servlets  Client Capable 1.0 Thu Aug 2 12:41:25 EDT 2007  ImplVersion: 2.5
                    Javax Transaction APIs  Client Capable 1.0 Thu Aug 2 12:42:14 EDT 2007  ImplVersion: 1.1
                    Java XML Registry 1.0 Wed Feb 6 15:01:03 PST 2008  ImplVersion: 1.0
                    Java XML Soap Extensions 1.3 Mon Jun 11 12:22:59 EDT 2007  ImplVersion: 1.3.1.0
                    Java Stream XML Extensions 1.1 Mon Jun 11 12:23:05 EDT 2007  ImplVersion: 1.1.1.0
                    Java API for XML-based RPC   1.2 Mon Jun 11 12:23:10 EDT 2007  ImplVersion: 1.2.1
                    WebLogic java compiler utils package Client Capable 1.2 Thu Feb 11 03:38:50 EST 2010  ImplVersion: 1.2.0.0
                    Weblogic Server Java Authentication Helper Classes Client Capable 1.1 Mon Jul 5 20:42:35 EDT 2010  ImplVersion: 1.1.0.0

                $java org.python.util.jython
                    *sys-package-mgr*: can't create package cache dir, '$PRODPATH1/wlserver_10.3/server/lib/
                        weblogic.jar/cachedir/packages'
                    Jython 2.2.1 on java1.7.0_191

            3) path of jython.jar, wlst.sh, weblogic.jar
                $PRODPATH1/oracle_common/util/jython/jython.jar
                $PRODPATH1/oracle_common/common/bin/wlst.sh
                $PRODPATH1/wlserver_10.3/common/bin/wlst.sh
                $PRODPATH1/wlserver_10.3/server/lib/weblogic.jar

            5.2. org.json.simple.* of Java in jython
            1) frequently-used packages:
                import org.json.simple.parser.JSONParser
                import org.json.simple.JSONObject
                import org.json.simple.JSONArray

            2) class content:
            dir(JSONParser()):
                ['S_END', 'S_INIT', 'S_IN_ARRAY', 'S_IN_ERROR', 'S_IN_FINISHED_VALUE', 'S_IN_OBJECT', 'S_IN_PAIR_VALUE',
                 'S_PASSED_PAIR_KEY', '__init__', 'class', 'equals', 'getClass', 'getPosition', 'hashCode',
                 'notify', 'notifyAll', 'parse', 'position', 'reset', 'toString', 'wait']
             <=> parse, class

            dir(JSONObject()):
                ['__init__', 'class', 'clear', 'clone', 'containsKey', 'containsValue', 'empty', 'entrySet', 'equals',
                'escape', 'get', 'getClass', 'hashCode', 'isEmpty', 'keySet', 'notify', 'notifyAll', 'put', 'putAll',
                'remove', 'size', 'toJSONString', 'toString', 'values', 'wait', 'writeJSONString']
            <=> get, keySet, values, entrySet, contains..., put..., remove, clear, ...empty,
                clone, class, size, to...String.

            dir(JSONArray()):
                ['__init__', 'add', 'addAll', 'class', 'clear', 'clone', 'contains', 'containsAll', 'empty',
                'ensureCapacity', 'equals', 'get', 'getClass', 'hashCode', 'indexOf', 'isEmpty', 'iterator',
                'lastIndexOf', 'listIterator', 'notify', 'notifyAll', 'remove', 'removeAll', 'retainAll',
                'set', 'size', 'subList', 'toArray', 'toJSONString', 'toString', 'trimToSize',
                'wait', 'writeJSONString']
            <=> get, set, ...iterator, add..., contains..., clear, ...empty,
                clone, class, size, to..., ...indexOf, subList.

        Notes: how to test in jython, more precisely in $java weblogic.WLST:
                on ... in ... POD:
                pushd /fsnadmin/aia/naliu/
                # export CLASSPATH=$PRODPATH1/wlserver_10.3/server/lib/weblogic.jar:${FASS_CLASSP}:$CLASSPATH
                export CLASSPATH=$PRODPATH2/modules/lib/json-simple-1.1.1.jar:$PRODPATH2/lib/natty-0.11.jar:$PRODPATH2/lib/antlr-runtime-3.5.2.jar:$PRODPATH2/lib/slf4j-api-1.7.10.jar:$PRODPATH1/jdk/:$CLASSPATH
                export WL_HOME=$PRODPATH1/wlserver_10.3
                export java=$PRODPATH1/jdk/bin/java
                . $WL_HOME/server/bin/setWLSEnv.sh
                $java weblogic.WLST datetime_parser_injy.py

    MODIFIED  (MM/DD/YY)
        Na  12/05/2018

"""
__VERSION__ = "1.0.0.12052018"


# imports
import os, os.path
import pprint as pp

# consts
CURRENT_DIR, SCRIPT_NAME = os.path.split(os.path.abspath(__file__))
DATA_PATH = os.path.join(CURRENT_DIR, r'data')
# for Shift+Alt+E
# CURRENT_PATH = os.getcwd()
# DATA_PATH = os.path.join(CURRENT_PATH, r'data')


"""linecache

"""
def try_linecache():
    import linecache

    fcsv = os.path.join(DATA_PATH, r'EEDM-MC_slow_report_in_bug28921682.csv')
    lines = linecache.getlines(fcsv)
    N = 10
    print('{} lines read from {}, top {}:\n'.format(len(lines), fcsv, N))
    pp.pprint(lines[:N])

    line_n = linecache.getline(filename=fcsv, lineno=N)
    print('Line {}:\n{}'.format(N, line_n))

    # if file was changed, .checkcache removed it from linecache.cache
    #   the method .checkcache returns None itself.
    linecache.checkcache(fcsv)
    # .updatecache read the files content in.
    lines2 = linecache.updatecache(fcsv)

    linecache.clearcache()
    print('empty list after .clearcache in linecache.cache:\n{}'.format(linecache.cache))

""" update a text file          
"""
def try_update_a_file():
    fxml = os.path.join(DATA_PATH, r'config.xml')

    # update on keys or patterns
    import tempfile
    fdt, ftmp = tempfile.mkstemp()
    os.close(fdt)
    N = 100
    import re
    re_p1 = re.compile(r'<name>(AdminServer)</name>')
    with open(fxml, 'rt') as fi, open(ftmp, 'wt') as fout:
        old = fi.read()
        old = re_p1.sub(r'<name>testing via two with statements: \1</name>', old)
        # works
        # old = old.replace(r'<name>AdminServer</name>',
        #             r'<name>testing via two with statements: AdminServer</name>')
        fout.write(old)

    # update on specific line
    # update a specific line, could use new variable or via mmap or via fileinput
    flipsum = os.path.join(DATA_PATH, r'lorem_ipsum.txt')
    import fileinput, sys
    for i, line in enumerate(fileinput.input(flipsum, inplace=True)):
        # replace
        # sys.stdout.write(line.replace('sit', 'SIT'))
        # add lineno
        print '%d: %s' % (fileinput.filelineno(), line),
        if i == 4:
            sys.stdout.write('\n')
        else:
            pass
    # close
    fileinput.close()

    # mmap: to insert into a file, no unicode strings handling
    import mmap
    def insert(filename, newstr, pos):
        if len(newstr) < 1:
            # do nothing
            return
        else:
            # insert newstr
            with open(filename, 'r+') as f:
                m = mmap.mmap(f.fileno(), os.path.getsize(filename))    # os.stat(filename).st_size
                size_orig = m.size()
                # check pos to insert
                if pos > size_orig:
                    pos = size_orig
                elif pos < 0:
                    pos = 0
                else:
                    pass
                size_newstr = len(newstr)
                m.resize(size_orig + size_newstr)
                m[pos+size_newstr:] = m[pos:size_orig]
                m[pos: pos+size_newstr] = newstr
                m.close()

    # on Linux
    os.system("sed -i s/foo/bar/ {}".format(flipsum))

    # or
    import shutil
    shutil.move(flipsum, flipsum+'~')
        # same as
    os.rename(flipsum, flipsum+'~')

    # ... update

""" natty    
"""
def try_natty():
    # works in Python2.7
    import natty
    dt_str = 'tomorrow'
    dparser = natty.DateParser(dt_str)
    print('natty.DateParser parses \033[1;31m{} \033[0m to \033[1;31m{} \033[0m.'.format(
        dt_str, dparser.result()))

    dt_str = 'monday and tuesday'
    dparser = natty.DateParser(dt_str)
    print('natty.DateParser parses \033[1;31m{} \033[0m to \033[1;31m{} \033[0m.'.format(
        dt_str, dparser.result()))

    # works in Jython
    import java.text.SimpleDateFormat as pfmt
    import java.util.Date as pdate
    import java.util.Locale as plocale
    import org.joda.time as jtime
    import org.joda.time.format as jfmt
    import org.joda.time.convert as jconvert
    import org.joda.time.base as jbase
    import org.joda.time.chrono as jchrono
    import org.joda.time.field as jfield
    import org.joda.time.tz as jtz

    ## import java.util.Date
    # import java.util.Calendar
    # import java.text.SimpleDateFormat
    from java.util import *

    # from com.joestelmach.natty import *
    import com.joestelmach.natty as natty
    from org.joda.time import *
    from org.joda.time.format import *

    # java.time.... only exists since Java 8, having joda-time concept
    # import java.time.temporal.ChronoUnit
    # import java.time.LocalDate



    # try natty
    # grammar for com.joestelmach.natty
    #   type(com.joestelmach.natty.Parser.parse(...).get(0).getDates().get(0)) is javainstance.
    # start_str = 'Fri Dec  7 07:35:55 UTC 2018'
    start_str = 'Mon Dec 10 07:58:56 UTC 2018'
    # parser = Parser()
    parser = natty.Parser()
    dts = parser.parse(start_str).get(0).getDates()
    res = dts.get(0)
    print('natty.Parser.parsed \033[1;31m%s\033[0m to \033[1;31m%s\033[0m.' % (start_str, res))
    # print('\toutput via res.toString():\t%s\ttimezoneOffset: %s' % (res.toString(), res.timezoneOffset))
    print('\toutput via res.toString():\t%s\n\toutput via res.toGMTString():\t%s\n\toutput via '
          'res.toLocaleString():\t%s' % (res.toString(), res.toGMTString(), res.toLocaleString()))
    print('\toutput via date:\t%s\n\toutput via time:\t%s' % (res.date, res.time))
    # check module contents
    print('\n\ttype(natty.Parser().parse(...).get(0).getDates().get(0)):\t%s' % (type(res)))
    print('\tdir(natty.Parser().parse(...).get(0).getDates().get(0)):\n\t%s\n' % (dir(res)))
    print('\n\tdir(natty):\n\t%s\n' % (dir(natty)))
    print('\n\tdir(java.util.Date):\n\t%s\n' % (dir(pdate)))
    print('\n\tdir(java.util.Locale):\n\t%s\n' % (dir(plocale)))
    print('\n\tdir(joda.time):\n\t%s\n' % (dir(jtime)))

    # try joda.time
    # get a DateTime
    jdt1 = DateTime(2012, 12, 15, 18, 23, 55, 02)
    print('org.joda.time: DateTime:\t%s' % (jdt1))
    print('\n\tdir(org.joda.time.DateTime):\n\t%s\n' % (dir(jdt1)))

    jdt2 = DateTime()
    print('joda.time.DateTime properties printout:\t%s' % (jdt2.monthOfYear().getAsText()))
    print('\t\t\t%s' % (jdt2.monthOfYear().getAsText()))
    print('\t\t\t%s' % (jdt2.dayOfWeek().getAsText(Locale.CHINESE)))
    print('\t\t\t%s' % (jdt2.monthOfYear().getAsShortText(Locale.CHINESE)))
    print('joda.time.DateTime properties reset to 0:\t%s' % (jdt2.dayOfWeek().roundCeilingCopy()))
    print('\t\t\t%s' % (jdt2.minuteOfDay().roundFloorCopy()))
    print('\t\t\t%s' % (jdt2.secondOfMinute().roundFloorCopy()))

    # check version of a java package
        # ref: https://stackoverflow.com/questions/21724145/get-jar-version-in-runtime
        # ref: https://mvnrepository.com/artifact/joda-time/joda-time/1.2.1
    print('\norg.joda.time.LocalDate was not existing in v1.2.1, but in v2.1.')
    print('joda.time package: SpecificationVersion: \033[1;31m%s\033[0m' % (jdt2.getClass().getPackage().getSpecificationVersion()))
    print('\t\t\tImplementationVersion: \033[1;31m%s\033[0m' % (jdt2.getClass().getPackage().getImplementationVersion()))

    # get daysBetween
    start = DateTime('2012-12-14')
    end = DateTime('2012-12-15')
    print('org.joda.time: DateTime:\t%s\t%s' % (start, end))
    pe = Period(start, end)
    years, mons, weeks, days, size, hours, mins, secs = pe.getYears(), pe.getMonths(), pe.getWeeks(), pe.getDays(), pe.size, pe.getHours(), pe.getMinutes(), pe.getSeconds()
    print('org.joda.time: from Period: %s years %s months %s weeks %s days %s hours %s minutes %s seconds %s millis' % (years, mons, weeks, days, hours, mins, secs, pe.getMillis()))
    print('org.joda.time: from Period: %s values\t%s toDurationFrom\t%s toDurationTo\n\t\t%s toDuration\t%stoString' % (pe.getValues(), pe.toDurationFrom(start), pe.toDurationTo(end), pe.toPeriod(), pe.toString()))
    print('org.joda.time: from Period: %s size\t%s PeriodType\t%sFieldsDifference' % (pe.size, pe.getPeriodType(), pe.fieldDifference))
    print('\n\tdir(org.joda.time.Period):\n\t%s\n' % (dir(pe)))

    # calculate a DateTime
    # date_str = DateTime().plusDays(18).plusMonths(1).toString()
    date_str = DateTime().plusDays(18).plusMonths(1).dayOfWeek().withMinimumValue().toString()
    print('DateTime().plusDays(18).plusMonths(1).dayOfWeek().withMinimumValue().toString():\t%s' % (date_str))

    # print out package content
    print('\n\tdir(org.joda.time.format):\n\t%s\n' % (dir(jfmt)))
    print('\n\tdir(org.joda.time.convert):\n\t%s\n' % (dir(jconvert)))
    print('\n\tdir(org.joda.time.base):\n\t%s\n' % (dir(jbase)))
    print('\n\tdir(org.joda.time.chrono):\n\t%s\n' % (dir(jchrono)))
    print('\n\tdir(org.joda.time.field):\n\t%s\n' % (dir(jfield)))
    print('\n\tdir(org.joda.time.tz):\n\t%s\n' % (dir(jtz)))

    # format
    fmt1 = DateTimeFormat.forPattern('yyyy-MM-dd HH:mm:ss')
    date_str = "2012-12-21 23:22:45"
    jdt_fmted = fmt1.parseDateTime(date_str)
    str1 = jdt_fmted.toString('yyyy/MM/dd HH:mm:ss EE')
    print('org.joda.time.format.DateTimeFormat: format converted from \033[1;31m%s \033[0mto\t\033[1;31m%s'
              '\033[0m.' % (date_str, str1))
    # print('org.joda.time: format converted from %s to\t%s' % (fmt1, str1))
    str1_c = jdt_fmted.toString('yyyy年MM月dd日 HH:mm:ss EE', Locale.CHINESE)
    print('\tto\t%s' % (str1_c))

    # convert calendar between JDK and joda-time
    java_cal1 = Calendar.getInstance()
    jdt_from_java = DateTime(java_cal1)
    print('org.joda.time: from Calendar:\t%s' % (jdt_from_java))
    jdt_from_java = jdt_from_java.plusYears(1).plusMonths(1).plusWeeks(1).plusDays(1).\
                        minusHours(1).minusMinutes(2).minusSeconds(1).minusMillis(1)
    print('org.joda.time: after +- daytime:\t%s' % (jdt_from_java))
    java_d2 = jdt_from_java.toDate()
    java_cal2 = jdt_from_java.toCalendar(Locale.CHINA)

""" try jpype
"""
def try_jpype():
    import jpype

    pp.pprint(dir(jpype))
    print('\n\n')
    res = jpype.startJVM(jpype.getDefaultJVMPath())
    print('jpype started JVM:\t{}'.format(res))
    print('jpype.isJVMStarted?\t{}'.format(jpype.isJVMStarted()))
    print('jpype.isThreadAttachedToJVM?\t{}'.format(jpype.isThreadAttachedToJVM()))
    res = jpype.shutdownJVM()
    print('jpype shutdown JVM:\t{}'.format(res))


"""try org.json.simple.*
"""
def try_simplejson():
    # JSON_STR as input str in JSON format to test json
    JSON_STR = """{
    	  "oid": {
    		"port": "port2",
    		"host": "host2",
    		"state": "OK"
    	  },
    	  "domains": [
    		{
    		  "servers": [
    			{
    			  "port": port3,
    			  "server_name": "AdminServer",
    			  "stdout": "domain_path1/servers/AdminServer/logs/AdminServer.out",
    			  "host": "host3",
    			  "state": "RUNNING"
    			},
    			{
    			  "port": port4,
    			  "server_name": "HomePageServer_1",
    			  "stdout": "domain_path4/servers/HomePageServer_1/logs/HomePageServer_1.out",
    			  "host": "host4",
    			  "state": "RUNNING"
    			}
    		  ],
    		  "state": "OK",
    		  "domain_name": "domain1"
    		}
    	  ],
    	  "state": "OK",
    	  "pod_name": "pod1"
    	  "db_conn": {
    		"db_instances": [
    		  {
    			"instance_url": "jdbc:oracle:thin:@db1:port1:instance1",
    			"state": "CONN_OK"
    		  }
    		],
    		"db_service": [
    		  {
    			"service_url": "jdbc:oracle:thin:@(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=db1)(PORT=port1)))(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=service1)(INSTANCE_NAME=instance1)))",
    			"state": "CONN_OK"
    		  }
    		],
    		"db_connecton_type": "MDS",
    		"state": "OK"
    	  }
    	}"""

    # check if python module json works?
    # <=> json module in python not working in jython 2.2.1.
    try:
        # import sys
        # sys.path.insert(1, '$PRODPATH3/PYTHON_BASE/python/lib/python2.7/site-packages/pandas/io/json')
        # # File "$PRODPATH3/PYTHON_BASE/python/lib/python2.7/site-packages/pandas/io/json/json.py", line 11
        # #         from pandas.io.common import (get_filepath_or_buffer, _get_handle,
        # #                                      ^
        # # SyntaxError: invalid syntax

        import json
        json_obj = json.loads(JSON_STR)
    except ImportError:
        print('Exception raised in import json:\n%s\nIgnore. Using org.json.simple.*.\n' % str(e))
        # do nothing
        pass

    import org.json.simple.parser.JSONParser as JSONParser
    import org.json.simple.JSONObject as JSONObject
    import org.json.simple.JSONArray as JSONArray

    # try JSONParser
    parser = JSONParser()
    json_obj = parser.parse(JSON_STR)
    print('str in JSON format after JSONParser().parse(JSON_STR):\n%s\n' % (json_obj))
    print('\ttype(json_obj):\t%s' % (type(json_obj)))    # <type 'javainstance'>
    print('\tjson_obj.class:\t%s\n' % (json_obj.class))    # org.json.simple.JSONObject
    print("dir(JSONParser().parse(JSON_STR)):\n%s\n" % (dir(json_obj)))

    # to get data from  <type 'javainstance'> of result of JSONParser.parse()
    oid_obj = json_obj['oid']
    print("json_obj['oid']:\t%s" % oid_obj)
    print("\tjson_obj['oid'] type:\t%s" % type(oid_obj))  # <type 'javainstance'>
    print('\toid_obj.class:\t%s\n' % (oid_obj.class))    # org.json.simple.JSONObject

    # print("\tjson_obj['oid']['host']:\t%s" % oid_obj['host'])
    # print("\tjson_obj['oid']['port']:\t%s" % oid_obj['port'])
    print("\ndir(json_obj['oid']):\n%s\n" % (dir(oid_obj)))
    oid_json_str = oid_obj.toJSONString()
    print("\t.toJSONString(), type:\t%s:\n\t%s\n" % (type(oid_json_str), oid_json_str))
    oid_str = oid_obj.toString()
    print("\t.toString(), type:\t%s:\n\t%s\n" % (type(oid_str), oid_str))
    print("\t.keySet:\t%s" % (oid_obj.keySet()))
    print("\t.values:\t%s\n" % (oid_obj.values()))
    print("\t.oid_obj.get('host'):\t%s\n" % (oid_obj.get('host')))
    # iterate
    for k, v in zip(oid_obj.keySet(), oid_obj.values()):
        print('\t%s: %s' % (k, v))

    # module info
    print("dir(JSONParser()):\n%s\n" % (dir(JSONParser())))
    print("dir(JSONObject()):\n%s\n" % (dir(JSONObject())))
    print("dir(JSONArray()):\n%s\n" % (dir(JSONArray())))

    # try JSONObject, JSONArray
    # copy domains -> servers here
    # [both work]
    # domains_obj = json_obj.get('domains')
    domains_obj = json_obj['domains']
    print("\ttype(domains_obj):\t%s" % (type(domains_obj)))  # <type 'javainstance'>
    print("\tdomains_obj.class:\t%s\n" % (domains_obj.class))  # org.json.simple.JSONArray
    print("domains_obj:\n%s\n" % (domains_obj))
    print("dir(domains_obj):\n%s\n" % (dir(domains_obj)))

    # [NOT work] b/c <type 'javainstance'>, should be Java Array type, no .get, [0] works.
    #   servers_obj = domains_obj.get('servers')
    servers_obj = domains_obj[0].get('servers')
    print("type(servers_obj):\t%s" % (type(servers_obj)))       # <type 'javainstance'>
    print("servers_obj.class:\t%s\n" % (servers_obj.class))     # org.json.simple.JSONArray
    print("servers_obj:\n%s\n" % (servers_obj))
    print("dir(servers_obj):\n%s\n" % (dir(servers_obj)))

    servers_arr = JSONArray()
    for server in servers_obj:
        # iterate over a list
        obj1 = JSONObject()
        print("\ttype(server):\t%s" % (type(server)))           # <type 'javainstance'>
        # [both work]
        print("\tserver.class:\t%s\n" % (server.class))           # org.json.simple.JSONObject
        # print("\tserver.getClass():\t%s\n" % (server.getClass())) # org.json.simple.JSONObject
        print("dir(server):\n%s\n" % (dir(server)))
        for entry in server.entrySet():
            # print("original entry in servers_obj.entrySet():\n%s" % (entry))    # server_name=AdminServer
            # print("\ttype(entry):\t%s" % (type(entry))) # <type 'javainstance'>
            # print("dir(entry):\n%s\n" % (dir(entry)))

            # [both work]
            # k, v = entry.toString().split('=')
            k, v = entry.key, entry.value
            obj1[k] = v
            # print("copied to obj1:\n%s\n" % (obj1))
        servers_arr.add(obj1)
    print("copied to servers_arr:\n%s\n" % (servers_arr))

    # clone domains_obj Java org.json.simple.JSONArray type to a new JSONArray
    domains_arr2 = domains_obj.clone()
    print("original: id(domains_obj):\t%s" % (id(domains_obj)))
    print("after domains_obj.clone(), id:\t%s,\tcontent:\n%s\n" % (id(domains_arr2), domains_arr2))
    # clone domains_obj Java org.json.simple.JSONArray type to a new JSONArray
    servers_arr2 = servers_obj.clone()
    print("original: id(servers_obj):\t%s" % (id(servers_obj)))
    print("after servers_obj.clone(), id:\t%s,\tcontent:\n%s\n" % (id(servers_arr2), servers_arr2))

    # clone server in servers_obj Java org.json.simple.JSONObject type to a new JSONObject
    for server in servers_obj:
        server_obj2 = server.clone()
        print("original: id(server):\t%s" % (id(server)))
        print("after server.clone(), id:\t%s,\tcontent:\n%s\n" % (id(server_obj2), server_obj2))



# main entry
def main():
    # linecache
    # try_linecache()
    # try_update_a_file()
    # try_jpype()
    # try_natty()
    try_simplejson()

    # TODO
    pass


# classes

# main entry
# if __name__ == "__main__":
#     main()
#
# Jython doesn't recognize __main__, not support '{}'.format
main()
