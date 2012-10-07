#!/bin/sh
PROG=${0##*/}
if [ $# = 2 ]; then
	# for using same syntax as rpm own find-lang
	RPM_BUILD_ROOT=$1
	shift
fi
dir=$RPM_BUILD_ROOT/usr/share/amsn
langfile=$1.lang
tmp=$(mktemp) || exit 1
rc=0

find $dir -type d -name lang > $tmp

echo '%defattr(644,root,root,755)' > $langfile
while read dir; do
	echo "%dir ${dir#$RPM_BUILD_ROOT}" >> $langfile
	for dir in $dir/*; do
		dir=${dir#$RPM_BUILD_ROOT}
		lang=${dir##*/lang}
		case "$lang" in
		zh-TW)
			lang=zh_TW
			;;
		zh-CN)
			lang=zh_CN
			;;
		al)
			lang=sq
			;;
		ca_VC)
			lang=ca
			;;
		ee)
			lang=et
			;;
		fri)
			lang=fy
			;;
		glg)
			lang=gl
			;;
		gr2)
			lang=el
			;;
		no)
			lang=nb
			;;
		ast)
			# no ISO 639-1 code present
			lang=NONE
			;;
		*-*)
			echo >&2 "ERROR: Need mapping for $lang!"
			rc=1
		;;
		esac
		echo "%lang($lang) ${dir#$RPM_BUILD_ROOT}" >> $langfile
	done
done < $tmp

if [ "$(egrep -v '(^%defattr|^$)' $langfile | wc -l)" -le 0 ]; then
	echo >&2 "$PROG: Error: international files not found!"
	rc=1
fi

rm -f $tmp
exit $rc
