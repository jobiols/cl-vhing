#!/usr/bin/env bash
# run test suite for vhing

CLIENT="vhing"

echo $CLIENT"_test"

oe -Q project_eng -c $CLIENT -d $CLIENT"_test"
